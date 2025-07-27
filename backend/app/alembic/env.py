import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, create_engine  # NOTE: create_engine instead of async
from alembic import context

# Add root to path so "backend" is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.core import config as app_config
from backend.app.database.session import Model  # your declarative base
from urllib.parse import urlparse

ASYNC_DB_URL = app_config.SQLALCHEMY_DATABASE_URL
SYNC_DB_URL = ASYNC_DB_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')



# this is the Alembic Config object
alembic_config = context.config
fileConfig(alembic_config.config_file_name)

# Sync URL (same URL, just used in sync mode)
alembic_config.set_main_option('sqlalchemy.url', SYNC_DB_URL)

target_metadata = Model.metadata


def run_migrations_offline():
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(SYNC_DB_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # optional: track column type changes
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
