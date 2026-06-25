import json
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.diagnostic_question import DiagnosticQuestion
from app.models.enums import BloomLevel, QuestionType, Subject


DEFAULT_DIAGNOSTIC_QUESTION_BANK_PATH = Path(__file__).resolve().parent / "data" / "diagnostic_questions.json"


def load_diagnostic_question_bank(path: Path = DEFAULT_DIAGNOSTIC_QUESTION_BANK_PATH) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def seed_diagnostic_question_bank(db: Session, *, reset: bool = False) -> tuple[int, int]:
    if reset:
        db.query(DiagnosticQuestion).delete()
        db.flush()

    created = 0
    updated = 0
    for payload in load_diagnostic_question_bank():
        subject = Subject(payload["subject"])
        bloom_level = BloomLevel(payload["bloom_level"])
        question_type = QuestionType(payload.get("question_type", QuestionType.MULTIPLE_CHOICE.value))

        existing = db.execute(
            select(DiagnosticQuestion).where(
                DiagnosticQuestion.subject == subject,
                DiagnosticQuestion.topic == payload["topic"],
                DiagnosticQuestion.bloom_level == bloom_level,
                DiagnosticQuestion.question_text == payload["question_text"],
            )
        ).scalar_one_or_none()

        values = {
            "subject": subject,
            "topic": payload["topic"],
            "skill": payload["skill"],
            "question_text": payload["question_text"],
            "bloom_level": bloom_level,
            "question_type": question_type,
            "options_json": payload["options_json"],
            "correct_answer": payload["correct_answer"],
            "explanation": payload.get("explanation"),
        }

        if existing:
            for key, value in values.items():
                setattr(existing, key, value)
            updated += 1
            continue

        db.add(DiagnosticQuestion(**values))
        created += 1

    return created, updated
