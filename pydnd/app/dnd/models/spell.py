"""SQLAlchemy Table: spell definition."""

from datetime import datetime

from app.dnd import schemas
from app.dnd.database.base_class import DbBase
from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship


class Spell(DbBase):
    """SQLAlchemy spell model."""

    # keys
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey(f"{schemas.enums.DbSchemaEnum.DND.value}.source.id"))
    # fields
    name = Column(String, nullable=False)
    casting_time = Column(String, nullable=False)
    classes = Column(ARRAY(String), nullable=False)
    components = Column(String, nullable=False)
    description = Column(String, nullable=False)
    duration = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    range = Column(String, nullable=False)
    ritual = Column(Boolean, nullable=False)
    school = Column(Enum(schemas.enums.SpellSchoolEnum, inherit_schema=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    created_by = Column(String, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        index=True,
        default=func.now(),
        onupdate=datetime.utcnow,
        nullable=False,
    )
    updated_by = Column(String, nullable=False)
    homebrew = Column(Boolean, default=True, nullable=False)
    # relationships
    source = relationship("Source")
    # constraints
    UniqueConstraint("source_id", "name", name="ux_spell")
