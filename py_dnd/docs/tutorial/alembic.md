# Alembic

## TEMP: init and init and init
### 0. `cd ~/ttrpg/ttrpg-api/py_dnd`
### 1. cleanup
* delete `alembic` folder
* delete revision in postgres `public/tables/alembic_version` table
* cleanup tables
```sql
-- clean up alembic revision
DELETE FROM public.alembic_version;
-- clean up dnd schema
DROP TABLE IF EXISTS dnd.jt_spell_to_class;
DROP TABLE IF EXISTS dnd.dnd_class;
DROP TABLE IF EXISTS dnd.spell;
DROP TABLE IF EXISTS dnd.source;
DROP SCHEMA IF EXISTS dnd;
-- clean up enums
DROP TYPE IF EXISTS spellcastingtimeenum;
DROP TYPE IF EXISTS spellschoolenum;
```
### 2. `poetry run alembic init alembic` create alembic folder
### 3. replace env.py

```python
"""Alembic env file for connecting to and manipilating database schemas."""
from logging.config import fileConfig

from alembic import context
from dnd import schemas
from dnd.core import uncached_settings
from dnd.database.base_class import DndSchemaBase
from sqlalchemy import engine_from_config, pool, text

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = DndSchemaBase.metadata

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
    return uncached_settings.POSTGRES_MASTER_URI


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
        create_schema = f"CREATE SCHEMA IF NOT EXISTS {schema_name}"
        connection.execute(text(create_schema))

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 4. `poetry run alembic revision --autogenerate -m "init"` generate first revision

### 5. `poetry run alembic upgrade head`
