"""snapshot diagnostic attempts and clean diagnostic metadata

Revision ID: 20260430_0008
Revises: 20260430_0007
Create Date: 2026-04-30 15:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260430_0008"
down_revision = "20260430_0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    selected_question_ids_type = sa.JSON().with_variant(postgresql.JSONB, "postgresql")

    op.alter_column("diagnostic_questions", "prompt", new_column_name="question_text")

    op.add_column("diagnostic_attempts", sa.Column("selected_question_ids", selected_question_ids_type, nullable=True))
    op.execute(
        """
        UPDATE diagnostic_attempts
        SET selected_question_ids = COALESCE(
            (
                SELECT jsonb_agg(diagnostic_questions.id ORDER BY diagnostic_questions.topic, diagnostic_questions.id)
                FROM diagnostic_questions
                WHERE diagnostic_questions.subject = diagnostic_attempts.subject
            ),
            '[]'::jsonb
        )
        """
    )
    op.alter_column("diagnostic_attempts", "selected_question_ids", nullable=False)

    op.drop_column("diagnostic_questions", "updated_at")
    op.drop_column("diagnostic_questions", "created_at")
    op.drop_column("diagnostic_responses", "updated_at")
    op.drop_column("diagnostic_responses", "created_at")
    op.drop_column("diagnostic_profiles", "updated_at")
    op.drop_column("diagnostic_profiles", "created_at")


def downgrade() -> None:
    op.add_column(
        "diagnostic_profiles",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.add_column(
        "diagnostic_profiles",
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.add_column(
        "diagnostic_responses",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.add_column(
        "diagnostic_responses",
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.add_column(
        "diagnostic_questions",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.add_column(
        "diagnostic_questions",
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    op.drop_column("diagnostic_attempts", "selected_question_ids")

    op.alter_column("diagnostic_questions", "question_text", new_column_name="prompt")
