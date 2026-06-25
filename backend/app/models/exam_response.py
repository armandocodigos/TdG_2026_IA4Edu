from sqlalchemy import Boolean, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin


class ExamResponse(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "exam_responses"
    __table_args__ = (
        UniqueConstraint("attempt_id", "question_id", name="uq_exam_responses_attempt_question"),
    )

    attempt_id: Mapped[str] = mapped_column(String(36), ForeignKey("exam_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("exam_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    answer_text: Mapped[str] = mapped_column(String(255), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    score_item: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    attempt = relationship("ExamAttempt", back_populates="responses")
    question = relationship("ExamQuestion", back_populates="responses")
