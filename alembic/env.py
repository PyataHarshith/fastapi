from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.database import Base
from app.config import settings

from configparser import ConfigParser

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.file_config = ConfigParser(interpolation=None)
# Option 2: Use Interpolation=None in the ConfigParser
# If you want to avoid escaping %, you can disable interpolation for the ConfigParser object entirely. Modify your env.py to create the ConfigParser without interpolation:
# with interpolation = none - @ = %40, without it @ = %%40-one % is to escape

# config.set_main_option("sqlalchemy.url", 'postgresql://postgres:Harshith%%402808@localhost:5432/fastapi')
# # DATABASE_PASSWORD=Harshith%402808 - when we use sqlalchemy 
# DATABASE_PASSWORD=Harshith%%402808 - when we use alembic


config.set_main_option("sqlalchemy.url", f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}")
# above line detects the database link through sqlalchemy database.py file - i think
# because we provided this "sqlalchemy.url" means giving info to detect or connect with sqlalchemy file(i.e, database.py)

# print(f"Using database URL: postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}")


#  in almebic to read @ - it is %%40

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# -------------------------------------check above changes

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
