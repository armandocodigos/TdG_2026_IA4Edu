from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import AttemptStatus, ExamDifficulty, MasteryLevel
from app.models.exam_attempt import ExamAttempt
from app.models.exam_response import ExamResponse
from app.models.exam_result import ExamResult
from app.models.user import User
from app.repositories.exam_repository import ExamRepository
from app.schemas.exam import (
    AnswerFeedbackRead,
    ExamAvailabilityItem,
    ExamAvailabilityResponse,
    ExamAttemptRead,
    ExamFinishResponse,
    ExamStartRequest,
    ExamQuestionRead,
    ExamResultRead,
    IncorrectAnswerFeedbackRead,
    LastExamResultRead,
)
from app.services.feedback_service import FeedbackService
from app.services.ollama_client import OllamaClient


class ExamService:
    def __init__(self, db: Session, ollama_client: OllamaClient | None = None) -> None:
        self.db = db
        self.repository = ExamRepository(db)
        self.ollama_client = ollama_client or OllamaClient()
        self.feedback_service = FeedbackService(ollama_client=self.ollama_client)

    def get_availability(self, user: User) -> ExamAvailabilityResponse:
        items = [
            ExamAvailabilityItem(topic=topic, difficulty=difficulty, question_count=count)
            for topic, difficulty, count in self.repository.list_question_availability(user.subject)
        ]
        return ExamAvailabilityResponse(subject=user.subject, items=items)

    def start_custom(self, *, user: User, payload: ExamStartRequest) -> ExamAttemptRead:
        topics = self._normalize_topics(payload)
        if not topics:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Selecciona al menos un tema para iniciar el examen.")
        if payload.question_count < 1 or payload.question_count > 15:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="La cantidad de preguntas debe estar entre 1 y 15.",
            )
        if payload.question_count < len(topics):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "La cantidad de preguntas debe ser al menos igual a la cantidad de temas seleccionados "
                    f"({len(topics)})."
                ),
            )

        available_count = self.repository.count_questions(
            subject=user.subject,
            topics=topics,
            difficulty=payload.difficulty,
        )
        available_by_topic = self.repository.count_questions_by_topic(
            subject=user.subject,
            topics=topics,
            difficulty=payload.difficulty,
        )
        unavailable_topics = [topic for topic in topics if available_by_topic.get(topic, 0) < 1]
        if unavailable_topics:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "No hay preguntas disponibles para todos los temas seleccionados en esa dificultad. "
                    f"Sin preguntas: {', '.join(unavailable_topics)}."
                ),
            )
        if available_count < payload.question_count:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "No hay suficientes preguntas para los temas y dificultad seleccionados. "
                    f"Disponibles: {available_count}; solicitadas: {payload.question_count}."
                ),
            )

        questions = self.repository.list_questions_for_exam_balanced(
            subject=user.subject,
            topics=topics,
            difficulty=payload.difficulty,
            limit=payload.question_count,
        )
        attempt = self.repository.create_attempt(
            ExamAttempt(
                user_id=user.id,
                subject=user.subject,
                status=AttemptStatus.IN_PROGRESS,
                topics=topics,
                difficulty=payload.difficulty,
                question_count=payload.question_count,
                selected_question_ids=[question.id for question in questions],
            )
        )
        self.db.commit()
        return self._build_attempt_read(
            attempt=attempt,
            title=self._build_exam_title(topics=topics, difficulty=payload.difficulty),
            questions=questions,
            topics=topics,
            difficulty=payload.difficulty,
            question_count=payload.question_count,
        )

    def _build_attempt_read(
        self,
        *,
        attempt: ExamAttempt,
        title: str,
        questions,
        topics: list[str] | None = None,
        difficulty: ExamDifficulty | None = None,
        question_count: int | None = None,
    ) -> ExamAttemptRead:
        return ExamAttemptRead(
            id=attempt.id,
            subject=attempt.subject,
            title=title,
            topics=topics or [],
            difficulty=difficulty,
            question_count=question_count or len(questions),
            questions=[
                ExamQuestionRead(
                    id=question.id,
                    topic=question.topic,
                    difficulty=question.difficulty,
                    skill=question.skill,
                    question_text=question.question_text,
                    options=question.options_json,
                    weight=question.weight,
                )
                for question in questions
            ],
        )

    def answer(self, *, user: User, attempt_id: str, question_id: str, answer: str) -> None:
        attempt = self._get_owned_attempt(user.id, attempt_id)
        if attempt.status != AttemptStatus.IN_PROGRESS:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El intento de examen ya fue cerrado.")

        question = self.repository.get_question(question_id)
        if not question or not self._question_belongs_to_attempt(attempt, question_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró la pregunta del examen.")

        response = self.repository.get_response(attempt_id, question_id)
        is_correct = answer.strip().lower() == question.correct_answer.strip().lower()
        score_item = question.weight if is_correct else 0.0

        if response:
            response.answer_text = answer
            response.is_correct = is_correct
            response.score_item = score_item
            self.repository.save_response(response)
        else:
            self.repository.save_response(
                ExamResponse(
                    attempt_id=attempt_id,
                    question_id=question_id,
                    answer_text=answer,
                    is_correct=is_correct,
                    score_item=score_item,
                )
            )
        self.db.commit()

    def finish(self, *, user: User, attempt_id: str) -> ExamFinishResponse:
        attempt = self._get_owned_attempt(user.id, attempt_id)
        if attempt.status != AttemptStatus.IN_PROGRESS:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El intento de examen ya fue cerrado.")
        if not attempt.responses:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El intento de examen no tiene respuestas.")

        topic_breakdown = self._compute_topic_breakdown(attempt.responses)
        attempt.status = AttemptStatus.COMPLETED
        attempt.score_global = self._compute_global_score(attempt.responses)

        strengths = [topic for topic, result in topic_breakdown.items() if result["mastery"] == MasteryLevel.HIGH.value]
        weaknesses = [topic for topic, result in topic_breakdown.items() if result["mastery"] == MasteryLevel.LOW.value]
        answers_feedback = self._build_answers_feedback(attempt.responses)
        incorrect_answers = [item for item in answers_feedback if not item["is_correct"]]
        positive_recommendations, improvement_recommendations = self.feedback_service.generate_split_recommendations(
            subject=attempt.subject.value,
            score_global=attempt.score_global,
            topic_breakdown=topic_breakdown,
            answers_feedback=answers_feedback,
            log_label="EXAM_FEEDBACK_SOURCE",
        )

        result = attempt.result
        if result is None:
            result = ExamResult(
                exam_attempt_id=attempt.id,
                score_global=attempt.score_global,
                topic_breakdown=topic_breakdown,
                strengths=strengths,
                weaknesses=weaknesses,
                positive_recommendations=positive_recommendations,
                improvement_recommendations=improvement_recommendations,
                incorrect_answers=incorrect_answers,
            )
        else:
            result.score_global = attempt.score_global
            result.topic_breakdown = topic_breakdown
            result.strengths = strengths
            result.weaknesses = weaknesses
            result.positive_recommendations = positive_recommendations
            result.improvement_recommendations = improvement_recommendations
            result.incorrect_answers = incorrect_answers
        self.repository.save_result(result)
        self.db.commit()
        result_read = ExamResultRead.model_validate(result)
        result_read.answers_feedback = [AnswerFeedbackRead.model_validate(item) for item in answers_feedback]
        return ExamFinishResponse(
            attempt_id=attempt.id,
            score_global=attempt.score_global,
            result=result_read,
        )

    def abandon(self, *, user: User, attempt_id: str) -> None:
        attempt = self._get_owned_attempt(user.id, attempt_id)
        if attempt.status == AttemptStatus.IN_PROGRESS:
            attempt.status = AttemptStatus.ABANDONED
            self.db.commit()

    def get_result(self, *, user: User, attempt_id: str) -> ExamResultRead:
        attempt = self._get_owned_attempt(user.id, attempt_id)
        if attempt.result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el resultado del examen.")
        return self._build_result_read(attempt)

    def get_latest_result(self, *, user: User) -> LastExamResultRead:
        attempt = self.repository.get_latest_completed_attempt(user.id)
        if not attempt or not attempt.result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aún no tienes un intento de examen completado.")

        topics = self._topics_from_attempt(attempt)
        difficulty = self._difficulty_from_attempt(attempt)
        return LastExamResultRead(
            attempt_id=attempt.id,
            subject=attempt.subject,
            title=self._build_exam_title(topics=topics, difficulty=difficulty),
            topics=topics,
            difficulty=difficulty,
            completed_at=attempt.updated_at.isoformat(),
            result=self._build_result_read(attempt),
        )

    def _get_owned_attempt(self, user_id: str, attempt_id: str) -> ExamAttempt:
        attempt = self.repository.get_attempt(attempt_id)
        if not attempt or attempt.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el intento de examen.")
        return attempt

    def _question_belongs_to_attempt(self, attempt: ExamAttempt, question_id: str) -> bool:
        return bool(attempt.selected_question_ids and question_id in attempt.selected_question_ids)

    def _normalize_topics(self, payload: ExamStartRequest) -> list[str]:
        topics: list[str] = []
        for topic in payload.topics:
            clean_topic = topic.strip()
            if clean_topic and clean_topic not in topics:
                topics.append(clean_topic)
        return topics

    def _topics_from_attempt(self, attempt: ExamAttempt) -> list[str]:
        if attempt.topics:
            return attempt.topics
        return sorted({response.question.topic for response in attempt.responses})

    def _difficulty_from_attempt(self, attempt: ExamAttempt) -> ExamDifficulty | None:
        if attempt.difficulty:
            return attempt.difficulty
        difficulties = {response.question.difficulty for response in attempt.responses}
        return next(iter(difficulties)) if len(difficulties) == 1 else None

    def _build_exam_title(self, *, topics: list[str], difficulty: ExamDifficulty | None) -> str:
        difficulty_label = {
            ExamDifficulty.BASIC: "básico",
            ExamDifficulty.INTERMEDIATE: "intermedio",
            ExamDifficulty.ADVANCED: "avanzado",
        }.get(difficulty, "mixto")
        topic_label = topics[0] if len(topics) == 1 else "varios temas"
        return f"Examen personalizado: {topic_label} ({difficulty_label})"

    def _compute_topic_breakdown(self, responses) -> dict[str, dict[str, float | int | str]]:
        by_topic: dict[str, dict[str, float]] = {}
        for response in responses:
            topic = response.question.topic
            accumulator = by_topic.setdefault(topic, {"score": 0.0, "max_score": 0.0, "correct": 0.0, "total": 0.0})
            accumulator["score"] += response.score_item
            accumulator["max_score"] += response.question.weight
            accumulator["correct"] += 1.0 if response.is_correct else 0.0
            accumulator["total"] += 1.0

        topic_breakdown: dict[str, dict[str, float | int | str]] = {}
        for topic, values in by_topic.items():
            score_percentage = round((values["score"] / values["max_score"]) * 100, 2) if values["max_score"] else 0.0
            mastery = self._score_to_mastery(score_percentage)
            topic_breakdown[topic] = {
                "mastery": mastery.value,
                "correct_answers": int(values["correct"]),
                "total_questions": int(values["total"]),
                "score_percentage": score_percentage,
            }
        return topic_breakdown

    def _compute_global_score(self, responses) -> float:
        score = sum(response.score_item for response in responses)
        max_score = sum(response.question.weight for response in responses)
        return round((score / max_score) * 100, 2) if max_score else 0.0

    def _score_to_mastery(self, score_percentage: float) -> MasteryLevel:
        if score_percentage >= 75:
            return MasteryLevel.HIGH
        if score_percentage >= 40:
            return MasteryLevel.MEDIUM
        return MasteryLevel.LOW

    def _build_result_read(self, attempt: ExamAttempt) -> ExamResultRead:
        result_read = ExamResultRead.model_validate(attempt.result)
        result_read.answers_feedback = [
            AnswerFeedbackRead.model_validate(item) for item in self._build_answers_feedback(attempt.responses)
        ]
        if not result_read.incorrect_answers:
            result_read.incorrect_answers = [
                IncorrectAnswerFeedbackRead.model_validate(item.model_dump())
                for item in result_read.answers_feedback
                if not item.is_correct
            ]
        return result_read

    def _build_answers_feedback(self, responses) -> list[dict[str, str | bool | None]]:
        feedback: list[dict[str, str | bool | None]] = []
        for response in responses:
            question = response.question
            feedback.append(
                {
                    "question_id": question.id,
                    "topic": question.topic,
                    "difficulty": question.difficulty.value,
                    "skill": question.skill,
                    "question_text": question.question_text,
                    "student_answer": response.answer_text,
                    "correct_answer": question.correct_answer,
                    "is_correct": response.is_correct,
                    "explanation": question.explanation,
                }
            )
        return feedback
