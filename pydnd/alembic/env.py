"""Alembic env file for connecting to and manipilating database schemas."""
from logging.config import fileConfig

from alembic import context
from dnd import schemas
from dnd.core import settings
from dnd.database.base import Base
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

target_metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)" "s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_db_uri() -> str:
    """Gets database connection string from app settings unless overridden.

    This string is pulled from the app settings unless you pass in a `-x db_override` argument.
    Example: `alembic -x db_override="foobar://connection.string"` upgrade head

    Returns:
        str: The database connection string.
    """
    db_override = context.get_x_argument(as_dictionary=True).get("db_override")
    if db_override:
        print("Alembic overriding db::", db_override)  # noqa: T001
        return db_override
    return settings.SQLALCHEMY_DATABASE_URI


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = get_db_uri()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        version_table="alembic_version",
        version_table_schema=schemas.enums.DbSchemaEnum.DND.value,  # <-- MATCH THE SCHEMA
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_db_uri()
    connectable = engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        schema_name = schemas.enums.DbSchemaEnum.DND.value
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            version_table="alembic_version",
            version_table_schema=schema_name,  # <-- MATCH THE SCHEMA
        )

        # Make sure our schema exists
        connection.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
