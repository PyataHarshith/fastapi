from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# database - # SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Harshith%402808@localhost:5432/fastapi'
# URL should be in the form of 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# if any special character used in password then use present encoding vakues eg: @ - %40
# @	%40
# :	%3A
# /	%2F

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


# when ever we deploy this project on any platform, if we hardcore our address like above then it's gonna expose to others and they can see our password
# to overcome above problem we use enviranment variables
# Environment variable - it is just a variable that you can configure on any computer, doesn't matter what operating system it is

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()

# for alembic library we import above base into env.py file i.e, present in alembic folder

# to connect sqlalchemy with alembic above four lines are important

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
