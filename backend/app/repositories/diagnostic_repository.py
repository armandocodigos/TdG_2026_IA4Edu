from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.diagnostic_attempt import DiagnosticAttempt
from app.models.diagnostic_profile import DiagnosticProfile
from app.models.diagnostic_question import DiagnosticQuestion
from app.models.diagnostic_response import DiagnosticResponse
from app.models.enums import AttemptStatus, Subject


class DiagnosticRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_questions_by_subject(self, subject: Subject) -> list[DiagnosticQuestion]:
        stmt = (
            select(DiagnosticQuestion)
            .where(DiagnosticQuestion.subject == subject)
            .order_by(DiagnosticQuestion.topic, DiagnosticQuestion.id)
        )
        return self.db.execute(stmt).scalars().all()

    def get_question(self, question_id: str) -> DiagnosticQuestion | None:
        return self.db.get(DiagnosticQuestion, question_id)

    def list_questions_by_ids(self, question_ids: list[str]) -> list[DiagnosticQuestion]:
        if not question_ids:
            return []

        stmt = select(DiagnosticQuestion).where(DiagnosticQuestion.id.in_(question_ids))
        questions_by_id = {question.id: question for question in self.db.execute(stmt).scalars().all()}
        return [questions_by_id[question_id] for question_id in question_ids if question_id in questions_by_id]

    def get_attempt(self, attempt_id: str) -> DiagnosticAttempt | None:
        stmt = (
            select(DiagnosticAttempt)
            .options(
                selectinload(DiagnosticAttempt.responses).selectinload(DiagnosticResponse.question),
            )
            .where(DiagnosticAttempt.id == attempt_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_in_progress_attempt(self, user_id: str) -> DiagnosticAttempt | None:
        stmt = select(DiagnosticAttempt).where(
            DiagnosticAttempt.user_id == user_id,
            DiagnosticAttempt.status == AttemptStatus.IN_PROGRESS,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_latest_completed_attempt(self, user_id: str, subject: Subject) -> DiagnosticAttempt | None:
        stmt = (
            select(DiagnosticAttempt)
            .options(
                selectinload(DiagnosticAttempt.responses).selectinload(DiagnosticResponse.question),
            )
            .where(
                DiagnosticAttempt.user_id == user_id,
                DiagnosticAttempt.subject == subject,
                DiagnosticAttempt.status == AttemptStatus.COMPLETED,
            )
            .order_by(DiagnosticAttempt.updated_at.desc(), DiagnosticAttempt.created_at.desc())
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def create_attempt(self, attempt: DiagnosticAttempt) -> DiagnosticAttempt:
        self.db.add(attempt)
        self.db.flush()
        self.db.refresh(attempt)
        return attempt

    def get_response(self, attempt_id: str, question_id: str) -> DiagnosticResponse | None:
        stmt = select(DiagnosticResponse).where(
            DiagnosticResponse.attempt_id == attempt_id,
            DiagnosticResponse.question_id == question_id,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def save_response(self, response: DiagnosticResponse) -> DiagnosticResponse:
        self.db.add(response)
        self.db.flush()
        self.db.refresh(response)
        return response

    def get_profile(self, user_id: str, subject: Subject) -> DiagnosticProfile | None:
        stmt = select(DiagnosticProfile).where(
            DiagnosticProfile.user_id == user_id,
            DiagnosticProfile.subject == subject,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def save_profile(self, profile: DiagnosticProfile) -> DiagnosticProfile:
        self.db.add(profile)
        self.db.flush()
        self.db.refresh(profile)
        return profile
