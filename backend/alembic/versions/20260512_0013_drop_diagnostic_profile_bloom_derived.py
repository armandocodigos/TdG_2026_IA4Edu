"""drop bloom-derived columns from diagnostic_profiles

Revision ID: 20260512_0013
Revises: 20260512_0012
Create Date: 2026-05-12 12:30:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260512_0013"
down_revision = "20260512_0012"
branch_labels = None
depends_on = None


DERIVED_COLUMNS = (
    "bloom_strengths",
    "bloom_weaknesses",
    "dominant_bloom_level",
    "highest_mastered_bloom_level",
)


def _json_type():
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        from sqlalchemy.dialects import postgresql

        return postgresql.JSONB()
    return sa.JSON()


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing = {column["name"] for column in inspector.get_columns("diagnostic_profiles")}

    for column_name in DERIVED_COLUMNS:
        if column_name in existing:
            op.drop_column("diagnostic_profiles", column_name)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing = {column["name"] for column in inspector.get_columns("diagnostic_profiles")}
    json_type = _json_type()
    can_alter_nullability = bind.dialect.name != "sqlite"
    bloom_enum = sa.Enum(
        "remember",
        "understand",
        "apply",
        "analyze",
        "evaluate",
        "create",
        name="bloom_level",
        create_type=False,
    )

    if "bloom_strengths" not in existing:
        op.add_column("diagnostic_profiles", sa.Column("bloom_strengths", json_type, nullable=True))
        op.execute("UPDATE diagnostic_profiles SET bloom_strengths = '[]'")
        if can_alter_nullability:
            op.alter_column("diagnostic_profiles", "bloom_strengths", nullable=False)

    if "bloom_weaknesses" not in existing:
        op.add_column("diagnostic_profiles", sa.Column("bloom_weaknesses", json_type, nullable=True))
        op.execute("UPDATE diagnostic_profiles SET bloom_weaknesses = '[]'")
        if can_alter_nullability:
            op.alter_column("diagnostic_profiles", "bloom_weaknesses", nullable=False)

    if "dominant_bloom_level" not in existing:
        op.add_column("diagnostic_profiles", sa.Column("dominant_bloom_level", bloom_enum, nullable=True))

    if "highest_mastered_bloom_level" not in existing:
        op.add_column("diagnostic_profiles", sa.Column("highest_mastered_bloom_level", bloom_enum, nullable=True))
