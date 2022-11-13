"""SQLAlchemy Table: source definition."""
from dnd.database.base_class import Base
from sqlalchemy import Column, Integer, String


class Source(Base):
    """SQLAlchemy source model."""

    # keys
    id = Column(Integer, primary_key=True, index=True)
    # fields
    name = Column(String, nullable=False, unique=True)
    short_name = Column(String, nullable=False, unique=True)
