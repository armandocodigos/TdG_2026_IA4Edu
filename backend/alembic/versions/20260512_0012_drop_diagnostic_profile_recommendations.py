"""drop legacy diagnostic_profile.recommendations

Revision ID: 20260512_0012
Revises: 20260504_0011
Create Date: 2026-05-12 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260512_0012"
down_revision = "20260504_0011"
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

    if "recommendations" in columns:
        op.drop_column("diagnostic_profiles", "recommendations")


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("diagnostic_profiles")}
    json_type = _json_type()
    can_alter_nullability = bind.dialect.name != "sqlite"

    if "recommendations" not in columns:
        op.add_column("diagnostic_profiles", sa.Column("recommendations", json_type, nullable=True))
        op.execute("UPDATE diagnostic_profiles SET recommendations = '[]'")
        if can_alter_nullability:
            op.alter_column("diagnostic_profiles", "recommendations", nullable=False)
