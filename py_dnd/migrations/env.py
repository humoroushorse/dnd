"""Alembic file for managing/running database migrations."""

import asyncio
import pathlib
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from py_dnd import shared
from py_dnd.core.config import Settings, get_settings
from py_dnd.database.base_class import DndSchemaBase
from py_dnd.features.sources.models import Source  # noqa: W0611
from py_dnd.features.spells.models import Spell  # noqa: W0611
from py_dnd.shared.enums import DbSchemaEnum

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

settings: Settings = get_settings()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = DndSchemaBase.metadata

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
    context.configure(
        url=settings.POSTGRES_DATABASE_URI,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=DbSchemaEnum.DND.value,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with your given database connection."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # connectable = AsyncEngine(
    #     engine_from_config(
    #         config.get_section(config.config_ini_section),
    #         prefix="sqlalchemy.",
    #         poolclass=pool.NullPool,
    #         future=True,
    #     )
    # )
    connectable = AsyncEngine(
        create_engine(
            settings.POSTGRES_DATABASE_URI,
            # echo=True,  # DEBUGGING
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {shared.enums.DbSchemaEnum.DND.value}"))
        await connection.commit()
        context.configure(
            url=settings.POSTGRES_DATABASE_URI,
            target_metadata=target_metadata,
            # literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            version_table_schema=DbSchemaEnum.DND.value,
        )
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
