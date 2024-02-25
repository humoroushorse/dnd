"""SQLAlchemy Table: source definition."""

from app.dnd.database.base_class import DbBase
from sqlalchemy import Column, Integer, String


class Source(DbBase):
    """SQLAlchemy source model."""

    # keys
    id = Column(Integer, primary_key=True, index=True)
    # fields
    name = Column(String, nullable=False, unique=True)
    short_name = Column(String, nullable=False, unique=True)
