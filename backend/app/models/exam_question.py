from sqlalchemy import Enum, Float, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin
from app.models.enums import ExamDifficulty, QuestionType, Subject, enum_values


class ExamQuestion(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "exam_questions"

    subject: Mapped[Subject] = mapped_column(
        Enum(Subject, name="subject", values_callable=enum_values),
        nullable=False,
        index=True,
    )
    topic: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    skill: Mapped[str] = mapped_column(String(200), nullable=False)
    difficulty: Mapped[ExamDifficulty] = mapped_column(
        Enum(ExamDifficulty, name="exam_difficulty", values_callable=enum_values),
        nullable=False,
        default=ExamDifficulty.BASIC,
        index=True,
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
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
    weight: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

    responses = relationship("ExamResponse", back_populates="question", cascade="all, delete-orphan")
