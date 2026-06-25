from sqlalchemy import Enum, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin
from app.models.enums import BloomLevel, QuestionType, Subject, enum_values


class DiagnosticQuestion(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "diagnostic_questions"

    subject: Mapped[Subject] = mapped_column(
        Enum(Subject, name="subject", values_callable=enum_values),
        nullable=False,
        index=True,
    )
    topic: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    skill: Mapped[str] = mapped_column(String(200), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    bloom_level: Mapped[BloomLevel] = mapped_column(
        Enum(BloomLevel, name="bloom_level", values_callable=enum_values),
        nullable=False,
        default=BloomLevel.UNDERSTAND,
    )
    question_type: Mapped[QuestionType] = mapped_column(
        Enum(QuestionType, name="question_type", values_callable=enum_values),
        nullable=False,
        default=QuestionType.MULTIPLE_CHOICE,
    )
    options_json: Mapped[list[str]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
        default=list,
    )
    correct_answer: Mapped[str] = mapped_column(String(255), nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)

    responses = relationship("DiagnosticResponse", back_populates="question", cascade="all, delete-orphan")
