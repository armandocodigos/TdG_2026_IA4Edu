"""drop legacy exam_results.recommendations

Revision ID: 20260513_0014
Revises: 20260512_0013
Create Date: 2026-05-13 09:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260513_0014"
down_revision = "20260512_0013"
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
    columns = {column["name"] for column in inspector.get_columns("exam_results")}

    if "recommendations" in columns:
        op.drop_column("exam_results", "recommendations")


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("exam_results")}
    json_type = _json_type()
    can_alter_nullability = bind.dialect.name != "sqlite"

    if "recommendations" not in columns:
        op.add_column("exam_results", sa.Column("recommendations", json_type, nullable=True))
        op.execute("UPDATE exam_results SET recommendations = '[]'")
        if can_alter_nullability:
            op.alter_column("exam_results", "recommendations", nullable=False)
