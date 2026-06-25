import argparse

import app.models
from app.core.database import SessionLocal
from scripts.diagnostic_question_bank import seed_diagnostic_question_bank


def main() -> None:
    parser = argparse.ArgumentParser(description="Carga el banco versionado de preguntas de diagnóstico.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Elimina las preguntas de diagnóstico existentes antes de cargar el banco versionado.",
    )
    args = parser.parse_args()

    db = SessionLocal()
    try:
        created, updated = seed_diagnostic_question_bank(db, reset=args.reset)
        db.commit()
    except Exception as exc:
        db.rollback()
        raise RuntimeError(f"No se pudo cargar el banco de preguntas de diagnóstico: {exc}") from exc
    finally:
        db.close()

    print(f"Diagnostic question bank seeded: created={created}, updated={updated}, reset={args.reset}")


if __name__ == "__main__":
    main()
