import json
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import ExamDifficulty, QuestionType, Subject
from app.models.exam_question import ExamQuestion


DEFAULT_EXAM_QUESTION_BANK_PATH = Path(__file__).resolve().parent / "data" / "exam_questions.json"


def load_exam_question_bank(path: Path = DEFAULT_EXAM_QUESTION_BANK_PATH) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def seed_exam_question_bank(db: Session, *, reset: bool = False) -> tuple[int, int]:
    if reset:
        db.query(ExamQuestion).delete()
        db.flush()

    created = 0
    updated = 0
    for payload in load_exam_question_bank():
        subject = Subject(payload["subject"])
        difficulty = ExamDifficulty(payload["difficulty"])
        question_type = QuestionType(payload.get("question_type", QuestionType.MULTIPLE_CHOICE.value))

        existing = db.execute(
            select(ExamQuestion).where(
                ExamQuestion.subject == subject,
                ExamQuestion.topic == payload["topic"],
                ExamQuestion.difficulty == difficulty,
                ExamQuestion.question_text == payload["question_text"],
            )
        ).scalar_one_or_none()

        values = {
            "subject": subject,
            "topic": payload["topic"],
            "skill": payload["skill"],
            "difficulty": difficulty,
            "question_text": payload["question_text"],
            "question_type": question_type,
            "options_json": payload["options_json"],
            "correct_answer": payload["correct_answer"],
            "explanation": payload.get("explanation"),
            "weight": payload["weight"],
        }

        if existing:
            for key, value in values.items():
                setattr(existing, key, value)
            updated += 1
            continue

        db.add(ExamQuestion(**values))
        created += 1

    return created, updated
