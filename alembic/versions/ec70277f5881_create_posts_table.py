"""create posts table

Revision ID: ec70277f5881
Revises: 
Create Date: 2024-11-28 03:15:09.663920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec70277f5881'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(), nullable = False, primary_key = True),
                            sa.Column('title', sa.String(),nullable = False))
    
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass

# alembic upgrade --help

# to make changes
# alembic upgrade (revision code provided above)

# alembic revision -m "--" - creates a file with description of change we gonna make

#  alembic heads - gives the revision code of latest file created in versions folder
# so to make changes of lastest file we can write (alembic upgrade head) instead of alembic upgrade revision code provided above

#  to rollback the change/revision
# alembic downgrade () or alembic downgrade -1
# -1 means one rollback, -2 means 2 rollbacks and so on

# if we rollback by 1 then to rollfront by 1 use - alembic upgrade +1

# alembic current

# alembic revision --autogenerate -m "" - this will check the models that we created in sqlalchemy, if anything is missed to create in alchemy it directs 
# detects the missings and generate them and it just creates the revision file, we have to upgrade it using alembic upgrade ()
# even if we make changes in sqlalchemy, run that command to auto generate/make changes