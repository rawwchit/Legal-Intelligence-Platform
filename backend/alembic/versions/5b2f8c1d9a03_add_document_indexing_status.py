"""add document indexing status

Revision ID: 5b2f8c1d9a03
Revises: a54a367bcf02
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "5b2f8c1d9a03"
down_revision: Union[str, Sequence[str], None] = "a54a367bcf02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "documents",
        sa.Column("indexing_status", sa.String(), nullable=False, server_default="pending"),
    )
    op.add_column(
        "documents",
        sa.Column("chunks_indexed", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column("documents", sa.Column("indexing_error", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("documents", "indexing_error")
    op.drop_column("documents", "chunks_indexed")
    op.drop_column("documents", "indexing_status")
