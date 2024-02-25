"""SQLAlchemy base for all the table creation models."""

import re
from typing import Any

from app.dnd import schemas
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class DbBase(DeclarativeBase):
    """SQLAlchemy model base that sets the schema and tablename.

    Table name is the model name but in snake case.

    Example:
        MyClassName becomes dnd.my_class_name in the database
    Returns:
        _type_: A base SQLAlchemy model for generating tables.
    """

    id: Any
    __name__: str

    __table_args__ = {
        "schema": schemas.enums.DbSchemaEnum.DND.value,
    }

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        # return self.__name__.lower()
        # e.g. SomeModelName -> some_model_name
        return re.sub(r"(?<!^)(?=[A-Z])", "_", self.__name__).lower()
