"""trim exam metadata and support abandoned attempts

Revision ID: 20260430_0006
Revises: 20260430_0005
Create Date: 2026-04-30 13:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260430_0006"
down_revision = "20260430_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("question_banks", "description")
    op.drop_column("question_banks", "updated_at")
    op.drop_column("question_banks", "created_at")

    op.drop_column("exam_questions", "updated_at")
    op.drop_column("exam_questions", "created_at")

    op.drop_column("exam_responses", "updated_at")
    op.drop_column("exam_responses", "created_at")

    op.drop_column("exam_results", "updated_at")
    op.drop_column("exam_results", "created_at")


def downgrade() -> None:
    op.add_column(
        "exam_results",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.add_column(
        "exam_results",
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    op.add_column(
        "exam_responses",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.add_column(
        "exam_responses",
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    op.add_column(
        "exam_questions",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.add_column(
        "exam_questions",
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    op.add_column(
        "question_banks",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.add_column(
        "question_banks",
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.add_column("question_banks", sa.Column("description", sa.Text(), nullable=True))
