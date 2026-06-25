"""drop diagnostic attempt question count

Revision ID: 20260430_0009
Revises: 20260430_0008
Create Date: 2026-04-30 15:30:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260430_0009"
down_revision = "20260430_0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("diagnostic_attempts")}
    if "question_count" in columns:
        op.drop_column("diagnostic_attempts", "question_count")


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("diagnostic_attempts")}
    if "question_count" not in columns:
        op.add_column("diagnostic_attempts", sa.Column("question_count", sa.Integer(), nullable=True))
        op.execute("UPDATE diagnostic_attempts SET question_count = jsonb_array_length(selected_question_ids)")
        op.alter_column("diagnostic_attempts", "question_count", nullable=False)
