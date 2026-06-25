from sqlalchemy import Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import AttemptStatus, Subject, enum_values


class DiagnosticAttempt(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "diagnostic_attempts"

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
    selected_question_ids: Mapped[list[str]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
        default=list,
    )

    user = relationship("User", back_populates="diagnostic_attempts")
    responses = relationship("DiagnosticResponse", back_populates="attempt", cascade="all, delete-orphan")
