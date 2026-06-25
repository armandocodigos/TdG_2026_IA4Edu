"""inline subject into exam questions

Revision ID: 20260430_0007
Revises: 20260430_0006
Create Date: 2026-04-30 14:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260430_0007"
down_revision = "20260430_0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    subject_ref = postgresql.ENUM(
        "precalculo",
        "preuniversitario",
        name="subject",
        create_type=False,
    )

    op.add_column("exam_questions", sa.Column("subject", subject_ref, nullable=True))
    op.execute(
        """
        UPDATE exam_questions
        SET subject = question_banks.subject
        FROM question_banks
        WHERE exam_questions.question_bank_id = question_banks.id
        """
    )
    op.alter_column("exam_questions", "subject", nullable=False)
    op.create_index(op.f("ix_exam_questions_subject"), "exam_questions", ["subject"], unique=False)

    op.drop_index(op.f("ix_exam_questions_question_bank_id"), table_name="exam_questions")
    op.drop_constraint("exam_questions_question_bank_id_fkey", "exam_questions", type_="foreignkey")
    op.drop_column("exam_questions", "question_bank_id")

    op.drop_index(op.f("ix_question_banks_subject"), table_name="question_banks")
    op.drop_table("question_banks")


def downgrade() -> None:
    subject_ref = postgresql.ENUM(
        "precalculo",
        "preuniversitario",
        name="subject",
        create_type=False,
    )

    op.create_table(
        "question_banks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("subject", subject_ref, nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
    )
    op.create_index(op.f("ix_question_banks_subject"), "question_banks", ["subject"], unique=False)
    op.execute(
        """
        INSERT INTO question_banks (id, subject, name)
        SELECT
            gen_random_uuid()::text,
            subject,
            CASE
                WHEN subject = 'precalculo' THEN 'Banco de preguntas de Precálculo'
                ELSE 'Banco de preguntas Preuniversitario'
            END
        FROM (SELECT DISTINCT subject FROM exam_questions) subjects
        """
    )

    op.add_column("exam_questions", sa.Column("question_bank_id", sa.String(length=36), nullable=True))
    op.execute(
        """
        UPDATE exam_questions
        SET question_bank_id = question_banks.id
        FROM question_banks
        WHERE exam_questions.subject = question_banks.subject
        """
    )
    op.alter_column("exam_questions", "question_bank_id", nullable=False)
    op.create_foreign_key(
        "exam_questions_question_bank_id_fkey",
        "exam_questions",
        "question_banks",
        ["question_bank_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(op.f("ix_exam_questions_question_bank_id"), "exam_questions", ["question_bank_id"], unique=False)

    op.drop_index(op.f("ix_exam_questions_subject"), table_name="exam_questions")
    op.drop_column("exam_questions", "subject")
