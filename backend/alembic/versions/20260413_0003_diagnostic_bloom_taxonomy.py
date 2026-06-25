"""add bloom taxonomy to diagnostic module

Revision ID: 20260413_0003
Revises: 20260405_0002
Create Date: 2026-04-13 12:30:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260413_0003"
down_revision = "20260405_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()

    bloom_level = postgresql.ENUM(
        "remember",
        "understand",
        "apply",
        "analyze",
        "evaluate",
        "create",
        name="bloom_level",
        create_type=True,
    )
    bloom_level.create(bind, checkfirst=True)

    bloom_level_ref = postgresql.ENUM(
        "remember",
        "understand",
        "apply",
        "analyze",
        "evaluate",
        "create",
        name="bloom_level",
        create_type=False,
    )

    op.add_column("diagnostic_questions", sa.Column("bloom_level", bloom_level_ref, nullable=True))
    op.execute("UPDATE diagnostic_questions SET bloom_level = 'understand' WHERE bloom_level IS NULL")
    op.alter_column("diagnostic_questions", "bloom_level", nullable=False)

    op.add_column("diagnostic_profiles", sa.Column("bloom_results", sa.JSON(), nullable=True))
    op.add_column("diagnostic_profiles", sa.Column("bloom_strengths", sa.JSON(), nullable=True))
    op.add_column("diagnostic_profiles", sa.Column("bloom_weaknesses", sa.JSON(), nullable=True))
    op.add_column("diagnostic_profiles", sa.Column("dominant_bloom_level", bloom_level_ref, nullable=True))
    op.add_column("diagnostic_profiles", sa.Column("highest_mastered_bloom_level", bloom_level_ref, nullable=True))

    op.execute("UPDATE diagnostic_profiles SET bloom_results = '{}' WHERE bloom_results IS NULL")
    op.execute("UPDATE diagnostic_profiles SET bloom_strengths = '[]' WHERE bloom_strengths IS NULL")
    op.execute("UPDATE diagnostic_profiles SET bloom_weaknesses = '[]' WHERE bloom_weaknesses IS NULL")

    op.alter_column("diagnostic_profiles", "bloom_results", nullable=False)
    op.alter_column("diagnostic_profiles", "bloom_strengths", nullable=False)
    op.alter_column("diagnostic_profiles", "bloom_weaknesses", nullable=False)


def downgrade() -> None:
    bind = op.get_bind()

    op.drop_column("diagnostic_profiles", "highest_mastered_bloom_level")
    op.drop_column("diagnostic_profiles", "dominant_bloom_level")
    op.drop_column("diagnostic_profiles", "bloom_weaknesses")
    op.drop_column("diagnostic_profiles", "bloom_strengths")
    op.drop_column("diagnostic_profiles", "bloom_results")
    op.drop_column("diagnostic_questions", "bloom_level")

    sa.Enum(name="bloom_level").drop(bind, checkfirst=True)
