import random

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.diagnostic_attempt import DiagnosticAttempt
from app.models.diagnostic_profile import DiagnosticProfile
from app.models.diagnostic_response import DiagnosticResponse
from app.models.enums import AttemptStatus, BloomLevel, MasteryLevel, get_bloom_weight
from app.models.user import User
from app.repositories.diagnostic_repository import DiagnosticRepository
from app.schemas.diagnostic import (
    DiagnosticAnswerFeedbackRead,
    DiagnosticAttemptReviewRead,
    DiagnosticAttemptRead,
    DiagnosticFinishResponse,
    DiagnosticProfileRead,
    DiagnosticQuestionRead,
)
from app.services.feedback_service import FeedbackService
from app.services.ollama_client import OllamaClient

DIAGNOSTIC_QUESTION_LIMIT = 10


class DiagnosticService:
    def __init__(self, db: Session, ollama_client: OllamaClient | None = None) -> None:
        self.db = db
        self.repository = DiagnosticRepository(db)
        self.feedback_service = FeedbackService(ollama_client=ollama_client)

    def start(self, user: User) -> DiagnosticAttemptRead:
        existing_attempt = self.repository.get_in_progress_attempt(user.id)
        if existing_attempt:
            existing_attempt.status = AttemptStatus.ABANDONED
            self.db.flush()

        questions = self.repository.list_questions_by_subject(user.subject)
        if not questions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay preguntas de diagnóstico configuradas para esta materia",
            )
        if len(questions) < DIAGNOSTIC_QUESTION_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "No hay suficientes preguntas para iniciar el diagnóstico. "
                    f"Disponibles: {len(questions)}; requeridas: {DIAGNOSTIC_QUESTION_LIMIT}."
                ),
            )

        questions = self._select_balanced_questions(questions, DIAGNOSTIC_QUESTION_LIMIT)
        selected_question_ids = [question.id for question in questions]

        attempt = self.repository.create_attempt(
            DiagnosticAttempt(
                user_id=user.id,
                subject=user.subject,
                status=AttemptStatus.IN_PROGRESS,
                selected_question_ids=selected_question_ids,
            )
        )
        self.db.commit()
        return self._build_attempt_read(attempt.id, user.subject, questions)

    def get_attempt(self, *, user: User, attempt_id: str) -> DiagnosticAttemptRead:
        attempt = self._get_owned_attempt(user.id, attempt_id)
        questions = self.repository.list_questions_by_ids(attempt.selected_question_ids)
        return self._build_attempt_read(
            attempt.id,
            attempt.subject,
            questions,
            status=attempt.status,
            answers={response.question_id: response.answer_text for response in attempt.responses},
        )

    def answer(self, *, user: User, attempt_id: str, question_id: str, answer: str) -> None:
        attempt = self._get_owned_attempt(user.id, attempt_id)
        if attempt.status != AttemptStatus.IN_PROGRESS:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El intento de diagnóstico ya fue cerrado")

        if question_id not in set(attempt.selected_question_ids):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La pregunta no pertenece a este intento de diagnóstico")

        question = self.repository.get_question(question_id)
        if not question or question.subject != user.subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró la pregunta de diagnóstico")

        response = self.repository.get_response(attempt_id, question_id)
        is_correct = answer.strip().lower() == question.correct_answer.strip().lower()
        score_item = get_bloom_weight(question.bloom_level) if is_correct else 0.0

        if response:
            response.answer_text = answer
            response.is_correct = is_correct
            response.score_item = score_item
            self.repository.save_response(response)
        else:
            self.repository.save_response(
                DiagnosticResponse(
                    attempt_id=attempt_id,
                    question_id=question_id,
                    answer_text=answer,
                    is_correct=is_correct,
                    score_item=score_item,
                )
            )
        self.db.commit()

    def finish(self, *, user: User, attempt_id: str) -> DiagnosticFinishResponse:
        attempt = self._get_owned_attempt(user.id, attempt_id)
        if attempt.status != AttemptStatus.IN_PROGRESS:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El intento de diagnóstico ya fue cerrado")

        selected_question_ids = set(attempt.selected_question_ids)
        answered_question_ids = {response.question_id for response in attempt.responses}
        answered_count = len(answered_question_ids.intersection(selected_question_ids))
        total_count = len(selected_question_ids)
        if answered_count < total_count:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Debes responder todas las preguntas antes de finalizar. Respondidas: {answered_count}/{total_count}",
            )

        topic_results = self._compute_topic_results(attempt.responses)
        bloom_results = self._compute_bloom_results(attempt.responses)
        if not topic_results or not bloom_results:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El intento de diagnóstico no tiene respuestas")

        attempt.status = AttemptStatus.COMPLETED
        attempt.score_global = self._compute_global_score(attempt.responses)

        strengths = [topic for topic, result in topic_results.items() if result["mastery"] == MasteryLevel.HIGH.value]
        weaknesses = [topic for topic, result in topic_results.items() if result["mastery"] == MasteryLevel.LOW.value]
        answers_feedback = self._build_answers_feedback(attempt.responses)
        positive_recommendations, improvement_recommendations = self.feedback_service.generate_split_recommendations(
            subject=user.subject.value,
            score_global=attempt.score_global,
            topic_breakdown=topic_results,
            answers_feedback=answers_feedback,
            log_label="DIAGNOSTIC_FEEDBACK_SOURCE",
        )

        profile = self.repository.get_profile(user.id, user.subject)
        if profile is None:
            profile = DiagnosticProfile(
                user_id=user.id,
                subject=user.subject,
                topic_results=topic_results,
                bloom_results=bloom_results,
                strengths=strengths,
                weaknesses=weaknesses,
                positive_recommendations=positive_recommendations,
                improvement_recommendations=improvement_recommendations,
            )
        else:
            profile.topic_results = topic_results
            profile.bloom_results = bloom_results
            profile.strengths = strengths
            profile.weaknesses = weaknesses
            profile.positive_recommendations = positive_recommendations
            profile.improvement_recommendations = improvement_recommendations
        self.repository.save_profile(profile)
        self.db.commit()
        return DiagnosticFinishResponse(
            attempt_id=attempt.id,
            score_global=attempt.score_global,
            profile=self._build_profile_read(profile),
            answers_feedback=[DiagnosticAnswerFeedbackRead.model_validate(item) for item in answers_feedback],
        )

    def abandon(self, *, user: User, attempt_id: str) -> None:
        attempt = self._get_owned_attempt(user.id, attempt_id)
        if attempt.status == AttemptStatus.IN_PROGRESS:
            attempt.status = AttemptStatus.ABANDONED
            self.db.commit()

    def get_result(self, *, user: User, attempt_id: str) -> DiagnosticFinishResponse:
        attempt = self._get_owned_attempt(user.id, attempt_id)
        if attempt.status != AttemptStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró el resultado del diagnóstico.",
            )
        profile = self.repository.get_profile(user.id, user.subject)
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró el perfil de diagnóstico.",
            )
        return DiagnosticFinishResponse(
            attempt_id=attempt.id,
            score_global=attempt.score_global or 0.0,
            profile=self._build_profile_read(profile),
            answers_feedback=[
                DiagnosticAnswerFeedbackRead.model_validate(item)
                for item in self._build_answers_feedback(attempt.responses)
            ],
        )

    def get_profile(self, user: User) -> DiagnosticProfileRead | None:
        profile = self.repository.get_profile(user.id, user.subject)
        if profile is None:
            return None
        return self._build_profile_read(profile)

    def get_latest_attempt_review(self, user: User) -> DiagnosticAttemptReviewRead | None:
        attempt = self.repository.get_latest_completed_attempt(user.id, user.subject)
        if attempt is None:
            return None
        return DiagnosticAttemptReviewRead(
            attempt_id=attempt.id,
            subject=attempt.subject,
            score_global=attempt.score_global or 0.0,
            answers_feedback=[
                DiagnosticAnswerFeedbackRead.model_validate(item)
                for item in self._build_answers_feedback(attempt.responses)
            ],
        )

    def _build_profile_read(self, profile: DiagnosticProfile) -> DiagnosticProfileRead:
        return DiagnosticProfileRead.model_validate(profile)

    def _get_owned_attempt(self, user_id: str, attempt_id: str) -> DiagnosticAttempt:
        attempt = self.repository.get_attempt(attempt_id)
        if not attempt or attempt.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el intento de diagnóstico")
        return attempt

    def _build_attempt_read(
        self,
        attempt_id: str,
        subject,
        questions,
        *,
        status: AttemptStatus = AttemptStatus.IN_PROGRESS,
        answers: dict[str, str] | None = None,
    ) -> DiagnosticAttemptRead:
        return DiagnosticAttemptRead(
            id=attempt_id,
            subject=subject,
            status=status,
            answers=answers or {},
            questions=[
                DiagnosticQuestionRead(
                    id=question.id,
                    topic=question.topic,
                    skill=question.skill,
                    question_text=question.question_text,
                    bloom_level=question.bloom_level,
                    options=question.options_json,
                )
                for question in questions
            ],
        )

    def _select_balanced_questions(self, questions, limit: int):
        remaining = list(questions)
        random.shuffle(remaining)
        selected = []
        topic_counts: dict[str, int] = {}
        bloom_counts: dict[BloomLevel, int] = {}

        while remaining and len(selected) < limit:
            min_topic_count = min(topic_counts.get(question.topic, 0) for question in remaining)
            topic_candidates = [
                question for question in remaining if topic_counts.get(question.topic, 0) == min_topic_count
            ]
            min_bloom_count = min(bloom_counts.get(question.bloom_level, 0) for question in topic_candidates)
            candidates = [
                question
                for question in topic_candidates
                if bloom_counts.get(question.bloom_level, 0) == min_bloom_count
            ]
            question = random.choice(candidates)
            selected.append(question)
            remaining.remove(question)
            topic_counts[question.topic] = topic_counts.get(question.topic, 0) + 1
            bloom_counts[question.bloom_level] = bloom_counts.get(question.bloom_level, 0) + 1

        random.shuffle(selected)
        return selected

    def _compute_topic_results(self, responses) -> dict[str, dict[str, float | int | str]]:
        return self._compute_breakdown(responses, key_builder=lambda response: response.question.topic)

    def _compute_bloom_results(self, responses) -> dict[str, dict[str, float | int | str]]:
        return self._compute_breakdown(responses, key_builder=lambda response: response.question.bloom_level.value)

    def _compute_breakdown(self, responses, *, key_builder) -> dict[str, dict[str, float | int | str]]:
        by_group: dict[str, dict[str, float]] = {}
        for response in responses:
            key = key_builder(response)
            weight = get_bloom_weight(response.question.bloom_level)
            accumulator = by_group.setdefault(key, {"score": 0.0, "max_score": 0.0, "correct": 0.0, "total": 0.0})
            accumulator["score"] += response.score_item
            accumulator["max_score"] += weight
            accumulator["correct"] += 1.0 if response.is_correct else 0.0
            accumulator["total"] += 1.0

        results: dict[str, dict[str, float | int | str]] = {}
        for key, values in by_group.items():
            score_percentage = round((values["score"] / values["max_score"]) * 100, 2) if values["max_score"] else 0.0
            mastery = self._score_to_mastery(score_percentage)
            results[key] = {
                "mastery": mastery.value,
                "correct_answers": int(values["correct"]),
                "total_questions": int(values["total"]),
                "score_percentage": score_percentage,
            }
        return results

    def _compute_global_score(self, responses) -> float:
        total_score = 0.0
        max_score = 0.0
        for response in responses:
            total_score += response.score_item
            max_score += get_bloom_weight(response.question.bloom_level)
        if max_score == 0:
            return 0.0
        return round((total_score / max_score) * 100, 2)

    def _build_answers_feedback(self, responses) -> list[dict[str, str | bool | None]]:
        feedback: list[dict[str, str | bool | None]] = []
        for response in responses:
            question = response.question
            feedback.append(
                {
                    "question_id": question.id,
                    "topic": question.topic,
                    "skill": question.skill,
                    "bloom_level": question.bloom_level,
                    "question_text": question.question_text,
                    "student_answer": response.answer_text,
                    "correct_answer": question.correct_answer,
                    "is_correct": response.is_correct,
                    "explanation": question.explanation,
                }
            )
        return feedback

    def _score_to_mastery(self, score_percentage: float) -> MasteryLevel:
        if score_percentage >= 75:
            return MasteryLevel.HIGH
        if score_percentage >= 40:
            return MasteryLevel.MEDIUM
        return MasteryLevel.LOW

