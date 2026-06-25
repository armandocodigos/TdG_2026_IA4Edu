"""add split diagnostic recommendations

Revision ID: 20260504_0011
Revises: 20260504_0010
Create Date: 2026-05-04 11:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260504_0011"
down_revision = "20260504_0010"
branch_labels = None
depends_on = None


def _json_type():
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        from sqlalchemy.dialects import postgresql

        return postgresql.JSONB()
    return sa.JSON()


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("diagnostic_profiles")}
    json_type = _json_type()
    can_alter_nullability = bind.dialect.name != "sqlite"

    if "positive_recommendations" not in columns:
        op.add_column("diagnostic_profiles", sa.Column("positive_recommendations", json_type, nullable=True))
        op.execute("UPDATE diagnostic_profiles SET positive_recommendations = '[]'")
        if can_alter_nullability:
            op.alter_column("diagnostic_profiles", "positive_recommendations", nullable=False)

    if "improvement_recommendations" not in columns:
        op.add_column("diagnostic_profiles", sa.Column("improvement_recommendations", json_type, nullable=True))
        op.execute("UPDATE diagnostic_profiles SET improvement_recommendations = recommendations")
        if can_alter_nullability:
            op.alter_column("diagnostic_profiles", "improvement_recommendations", nullable=False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("diagnostic_profiles")}

    if "improvement_recommendations" in columns:
        op.drop_column("diagnostic_profiles", "improvement_recommendations")
    if "positive_recommendations" in columns:
        op.drop_column("diagnostic_profiles", "positive_recommendations")
