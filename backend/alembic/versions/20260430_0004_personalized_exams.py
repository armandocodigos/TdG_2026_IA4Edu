"""add personalized exam fields

Revision ID: 20260430_0004
Revises: 20260413_0003
Create Date: 2026-04-30 10:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260430_0004"
down_revision = "20260413_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    exam_difficulty = postgresql.ENUM(
        "basic",
        "intermediate",
        "advanced",
        name="exam_difficulty",
        create_type=True,
    )
    exam_difficulty.create(bind, checkfirst=True)
    exam_difficulty_ref = postgresql.ENUM(
        "basic",
        "intermediate",
        "advanced",
        name="exam_difficulty",
        create_type=False,
    )

    op.add_column("exam_questions", sa.Column("difficulty", exam_difficulty_ref, nullable=True))
    op.execute("UPDATE exam_questions SET difficulty = 'basic' WHERE difficulty IS NULL")
    op.alter_column("exam_questions", "difficulty", nullable=False)
    op.create_index(op.f("ix_exam_questions_difficulty"), "exam_questions", ["difficulty"], unique=False)

    op.add_column("exam_attempts", sa.Column("selected_question_ids", sa.JSON(), nullable=True))
    op.add_column("exam_results", sa.Column("incorrect_answers", sa.JSON(), nullable=True))
    op.execute("UPDATE exam_results SET incorrect_answers = '[]' WHERE incorrect_answers IS NULL")
    op.alter_column("exam_results", "incorrect_answers", nullable=False)


def downgrade() -> None:
    bind = op.get_bind()

    op.drop_column("exam_results", "incorrect_answers")
    op.drop_column("exam_attempts", "selected_question_ids")
    op.drop_index(op.f("ix_exam_questions_difficulty"), table_name="exam_questions")
    op.drop_column("exam_questions", "difficulty")

    sa.Enum(name="exam_difficulty").drop(bind, checkfirst=True)
