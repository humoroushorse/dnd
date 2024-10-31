"""SQLAlchemy Table: dnd_class definition."""

from dnd.database.base_class import DbBase
from dnd.schemas.enums import DbSchemaEnum
from sqlalchemy import ARRAY, Column, ForeignKey, String
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DndClass(DbBase):
    """SQLAlchemy dnd_class model."""

    # keys
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source_id: Mapped[int] = mapped_column(ForeignKey(f"{DbSchemaEnum.DND.value}.source.id"))
    # fields
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    hit_die: Mapped[str] = mapped_column(nullable=False)
    primary_ability: Mapped[str] = mapped_column(nullable=False)
    saving_throw_proficiencies: Mapped[str] = mapped_column(nullable=False)
    armor_proficiencies = Column(MutableList.as_mutable(ARRAY(String)), nullable=False)
    shield_proficiencies = Column(MutableList.as_mutable(ARRAY(String)), nullable=False)
    weapon_proficiencies = Column(MutableList.as_mutable(ARRAY(String)), nullable=False)
    # relationships
    source = relationship("Source")
