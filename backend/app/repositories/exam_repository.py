import random

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.enums import AttemptStatus, ExamDifficulty, Subject
from app.models.exam_attempt import ExamAttempt
from app.models.exam_question import ExamQuestion
from app.models.exam_response import ExamResponse
from app.models.exam_result import ExamResult


class ExamRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_question_availability(self, subject: Subject) -> list[tuple[str, ExamDifficulty, int]]:
        stmt = (
            select(ExamQuestion.topic, ExamQuestion.difficulty, func.count(ExamQuestion.id))
            .where(ExamQuestion.subject == subject)
            .group_by(ExamQuestion.topic, ExamQuestion.difficulty)
            .order_by(ExamQuestion.topic, ExamQuestion.difficulty)
        )
        return [(topic, difficulty, count) for topic, difficulty, count in self.db.execute(stmt).all()]

    def count_questions(self, *, subject: Subject, topics: list[str], difficulty: ExamDifficulty) -> int:
        stmt = (
            select(func.count(ExamQuestion.id))
            .where(
                ExamQuestion.subject == subject,
                ExamQuestion.topic.in_(topics),
                ExamQuestion.difficulty == difficulty,
            )
        )
        return self.db.execute(stmt).scalar_one()

    def list_questions_for_exam_balanced(
        self,
        *,
        subject: Subject,
        topics: list[str],
        difficulty: ExamDifficulty,
        limit: int,
    ) -> list[ExamQuestion]:
        selected: list[ExamQuestion] = []

        for topic in topics:
            stmt = (
                select(ExamQuestion)
                .where(
                    ExamQuestion.subject == subject,
                    ExamQuestion.topic == topic,
                    ExamQuestion.difficulty == difficulty,
                )
                .order_by(func.random())
                .limit(1)
            )
            question = self.db.execute(stmt).scalar_one_or_none()
            if question is not None:
                selected.append(question)

        remaining_limit = limit - len(selected)
        if remaining_limit > 0:
            selected_ids = [question.id for question in selected]
            stmt = (
                select(ExamQuestion)
                .where(
                    ExamQuestion.subject == subject,
                    ExamQuestion.topic.in_(topics),
                    ExamQuestion.difficulty == difficulty,
                )
                .order_by(func.random())
                .limit(remaining_limit)
            )
            if selected_ids:
                stmt = stmt.where(ExamQuestion.id.notin_(selected_ids))
            selected.extend(self.db.execute(stmt).scalars().all())

        random.shuffle(selected)
        return selected

    def count_questions_by_topic(
        self,
        *,
        subject: Subject,
        topics: list[str],
        difficulty: ExamDifficulty,
    ) -> dict[str, int]:
        stmt = (
            select(ExamQuestion.topic, func.count(ExamQuestion.id))
            .where(
                ExamQuestion.subject == subject,
                ExamQuestion.topic.in_(topics),
                ExamQuestion.difficulty == difficulty,
            )
            .group_by(ExamQuestion.topic)
        )
        return {topic: count for topic, count in self.db.execute(stmt).all()}

    def create_attempt(self, attempt: ExamAttempt) -> ExamAttempt:
        self.db.add(attempt)
        self.db.flush()
        self.db.refresh(attempt)
        return attempt

    def get_attempt(self, attempt_id: str) -> ExamAttempt | None:
        stmt = (
            select(ExamAttempt)
            .options(
                selectinload(ExamAttempt.responses).selectinload(ExamResponse.question),
                selectinload(ExamAttempt.result),
            )
            .where(ExamAttempt.id == attempt_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_latest_completed_attempt(self, user_id: str) -> ExamAttempt | None:
        stmt = (
            select(ExamAttempt)
            .options(
                selectinload(ExamAttempt.responses).selectinload(ExamResponse.question),
                selectinload(ExamAttempt.result),
            )
            .where(
                ExamAttempt.user_id == user_id,
                ExamAttempt.status == AttemptStatus.COMPLETED,
                ExamAttempt.result.has(),
            )
            .order_by(ExamAttempt.updated_at.desc(), ExamAttempt.created_at.desc())
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_question(self, question_id: str) -> ExamQuestion | None:
        return self.db.get(ExamQuestion, question_id)

    def get_response(self, attempt_id: str, question_id: str) -> ExamResponse | None:
        stmt = select(ExamResponse).where(
            ExamResponse.attempt_id == attempt_id,
            ExamResponse.question_id == question_id,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def save_response(self, response: ExamResponse) -> ExamResponse:
        self.db.add(response)
        self.db.flush()
        self.db.refresh(response)
        return response

    def save_result(self, result: ExamResult) -> ExamResult:
        self.db.add(result)
        self.db.flush()
        self.db.refresh(result)
        return result
