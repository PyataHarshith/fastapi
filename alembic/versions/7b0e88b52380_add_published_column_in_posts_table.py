"""add published column in posts table

Revision ID: 7b0e88b52380
Revises: 69c842feb012
Create Date: 2024-11-28 11:57:44.296135

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b0e88b52380'
down_revision: Union[str, None] = '69c842feb012'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(),nullable=False, default=True))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    pass
