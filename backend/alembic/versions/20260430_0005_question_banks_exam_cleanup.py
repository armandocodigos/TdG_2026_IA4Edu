"""rename exam templates to question banks

Revision ID: 20260430_0005
Revises: 20260430_0004
Create Date: 2026-04-30 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260430_0005"
down_revision = "20260430_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    exam_difficulty_ref = postgresql.ENUM(
        "basic",
        "intermediate",
        "advanced",
        name="exam_difficulty",
        create_type=False,
    )

    op.drop_constraint("exam_questions_exam_template_id_fkey", "exam_questions", type_="foreignkey")
    op.drop_constraint("exam_attempts_exam_template_id_fkey", "exam_attempts", type_="foreignkey")
    op.drop_index("ix_exam_questions_exam_template_id", table_name="exam_questions")
    op.drop_index("ix_exam_attempts_exam_template_id", table_name="exam_attempts")

    op.rename_table("exam_templates", "question_banks")
    op.drop_index("ix_exam_templates_subject", table_name="question_banks")
    op.drop_index("ix_exam_templates_topic", table_name="question_banks")
    op.alter_column("question_banks", "title", new_column_name="name")
    op.drop_column("question_banks", "topic")
    op.drop_column("question_banks", "is_integrator")
    op.create_index(op.f("ix_question_banks_subject"), "question_banks", ["subject"], unique=False)

    op.alter_column("exam_questions", "exam_template_id", new_column_name="question_bank_id")
    op.alter_column("exam_questions", "prompt", new_column_name="question_text")
    op.create_foreign_key(
        "exam_questions_question_bank_id_fkey",
        "exam_questions",
        "question_banks",
        ["question_bank_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(op.f("ix_exam_questions_question_bank_id"), "exam_questions", ["question_bank_id"], unique=False)

    op.add_column("exam_attempts", sa.Column("topics", sa.JSON(), nullable=True))
    op.add_column("exam_attempts", sa.Column("difficulty", exam_difficulty_ref, nullable=True))
    op.add_column("exam_attempts", sa.Column("question_count", sa.Integer(), nullable=True))
    op.drop_column("exam_attempts", "exam_template_id")


def downgrade() -> None:
    op.add_column("exam_attempts", sa.Column("exam_template_id", sa.String(length=36), nullable=True))
    op.drop_column("exam_attempts", "question_count")
    op.drop_column("exam_attempts", "difficulty")
    op.drop_column("exam_attempts", "topics")

    op.drop_index(op.f("ix_exam_questions_question_bank_id"), table_name="exam_questions")
    op.drop_constraint("exam_questions_question_bank_id_fkey", "exam_questions", type_="foreignkey")
    op.alter_column("exam_questions", "question_text", new_column_name="prompt")
    op.alter_column("exam_questions", "question_bank_id", new_column_name="exam_template_id")

    op.drop_index(op.f("ix_question_banks_subject"), table_name="question_banks")
    op.add_column("question_banks", sa.Column("is_integrator", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("question_banks", sa.Column("topic", sa.String(length=200), nullable=True))
    op.alter_column("question_banks", "name", new_column_name="title")
    op.rename_table("question_banks", "exam_templates")

    op.create_index("ix_exam_templates_topic", "exam_templates", ["topic"], unique=False)
    op.create_index("ix_exam_templates_subject", "exam_templates", ["subject"], unique=False)
    op.create_index("ix_exam_questions_exam_template_id", "exam_questions", ["exam_template_id"], unique=False)
    op.create_index("ix_exam_attempts_exam_template_id", "exam_attempts", ["exam_template_id"], unique=False)
    op.create_foreign_key(
        "exam_questions_exam_template_id_fkey",
        "exam_questions",
        "exam_templates",
        ["exam_template_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "exam_attempts_exam_template_id_fkey",
        "exam_attempts",
        "exam_templates",
        ["exam_template_id"],
        ["id"],
        ondelete="CASCADE",
    )
