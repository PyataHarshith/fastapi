"""add content column to posts table

Revision ID: 69c842feb012
Revises: ec70277f5881
Create Date: 2024-11-28 03:46:00.708244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69c842feb012'
down_revision: Union[str, None] = 'ec70277f5881'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass


# to add foreign key
# op.add_column(-----)
# op.create_foreign_key('post_foreign_key', source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
