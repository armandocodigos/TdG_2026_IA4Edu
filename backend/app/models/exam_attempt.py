from sqlalchemy import Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import AttemptStatus, ExamDifficulty, Subject, enum_values


class ExamAttempt(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "exam_attempts"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject: Mapped[Subject] = mapped_column(
        Enum(Subject, name="subject", values_callable=enum_values),
        nullable=False,
        index=True,
    )
    status: Mapped[AttemptStatus] = mapped_column(
        Enum(AttemptStatus, name="attempt_status", values_callable=enum_values),
        nullable=False,
        default=AttemptStatus.IN_PROGRESS,
    )
    score_global: Mapped[float | None] = mapped_column(Float, nullable=True)
    topics: Mapped[list[str] | None] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=True,
    )
    difficulty: Mapped[ExamDifficulty | None] = mapped_column(
        Enum(ExamDifficulty, name="exam_difficulty", values_callable=enum_values),
        nullable=True,
    )
    question_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    selected_question_ids: Mapped[list[str] | None] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=True,
    )

    user = relationship("User", back_populates="exam_attempts")
    responses = relationship("ExamResponse", back_populates="attempt", cascade="all, delete-orphan")
    result = relationship("ExamResult", back_populates="attempt", uselist=False, cascade="all, delete-orphan")
