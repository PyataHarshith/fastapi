from ..database import Base
# base is object of declarative_base class
from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,String,Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .usermodels import User

class Post(Base):
    __tablename__ = "posts_python"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,nullable = False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User")


# this makes sure that it will create the table with the given name only when a table with that name doesn't exists


class Votes(Base):
    __tablename__ = "votes"

    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer,ForeignKey("posts_python.id", ondelete="CASCADE"), primary_key=True)
    # post = relationship("Post")

# so if we create another column in Post now it won't be added in postgres database- this is the limitation of sqlalchemy
#  so we use another library called Alembic - which is more powerful and can able to update the tables anytime and maintains the record
#  alembic --help
# alembic init alembic - creates an alembic db folder in present directory(i.e, in FAST API folder)
# alembic revision --help
# alembic - it is like an extension of sqlalchemy

