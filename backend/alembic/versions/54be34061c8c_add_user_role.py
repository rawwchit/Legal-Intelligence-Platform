"""add user role

Revision ID: 54be34061c8c
Revises: f9d2b28be9b0
Create Date: 2026-07-16 13:56:59.723246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54be34061c8c'
down_revision: Union[str, Sequence[str], None] = 'f9d2b28be9b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    user_role = sa.Enum('ADMIN', 'LAWYER', 'CLIENT', name='userrole')
    user_role.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.Enum('ADMIN', 'LAWYER', 'CLIENT', name='userrole'),
            nullable=False,
            server_default='CLIENT',
        ),
    )

    op.alter_column('users', 'role', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'role')
    sa.Enum('ADMIN', 'LAWYER', 'CLIENT', name='userrole').drop(op.get_bind(), checkfirst=True)
