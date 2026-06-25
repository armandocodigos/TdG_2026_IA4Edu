import app.models
from app.core.database import SessionLocal
from app.models.diagnostic_question import DiagnosticQuestion
from app.models.exam_question import ExamQuestion
from scripts.diagnostic_question_bank import seed_diagnostic_question_bank
from scripts.exam_question_bank import seed_exam_question_bank


def seed_diagnostic_questions(db) -> int:
    created, _updated = seed_diagnostic_question_bank(db)
    return created


def seed_exam(db) -> int:
    created, _updated = seed_exam_question_bank(db)
    return created


def clear_existing_questions(db) -> None:
    db.query(DiagnosticQuestion).delete()
    db.query(ExamQuestion).delete()
    db.flush()


def main() -> None:
    db = SessionLocal()
    diagnostic_created = 0
    exam_questions_created = 0
    try:
        print("Borrando preguntas y bancos anteriores...")
        clear_existing_questions(db)
        
        print("Sembrando nuevas preguntas...")
        diagnostic_created = seed_diagnostic_questions(db)
        exam_questions_created = seed_exam(db)
        db.commit()
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

    print(
        "Seed completed: "
        f"diagnostic_questions={diagnostic_created}, "
        f"exam_questions={exam_questions_created}"
    )


if __name__ == "__main__":
    main()
