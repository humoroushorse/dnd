"""SQLAlchemy base for all the table creation models."""

from typing import Any

from sqlalchemy import JSON, MetaData
from sqlalchemy.orm import DeclarativeBase

from py_dnd.shared.enums import DbSchemaEnum

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class DndSchemaBase(DeclarativeBase):
    """SQLAlchemy model base that sets the schema and tablename.

    Table name is the model name but in snake case.

    Example:
        MyClassName becomes py_dnd.my_class_name in the database
    Returns:
        _type_: A base SQLAlchemy model for generating tables.
    """

    id: Any
    __name__: str

    __table_args__: tuple | dict = {
        "schema": DbSchemaEnum.DND.value,
    }

    type_annotation_map = {dict[str, Any]: JSON}

    metadata = MetaData(naming_convention=naming_convention)

    # # Generate __tablename__ automatically
    # @declared_attr
    # def __tablename__(self) -> str:
    #     # return self.__name__.lower()
    #     # e.g. SomeModelName -> some_model_name
    #     return re.sub(r"(?<!^)(?=[A-Z])", "_", self.__name__).lower()

    def __repr__(self) -> str:
        columns = ", ".join([f"{k}={repr(v)}" for k, v in self.__dict__.items() if not k.startswith("_")])
        return f"<{self.__class__.__name__}({columns})>"
