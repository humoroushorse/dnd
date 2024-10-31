"""SQLAlchemy Table: spell definition."""

import datetime

from dnd.database.base_class import DbBase
from dnd.schemas.enums import DbSchemaEnum, SpellSchoolEnum
from sqlalchemy import ARRAY, Column, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Spell(DbBase):
    """SQLAlchemy spell model."""

    # keys
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source_id: Mapped[int] = mapped_column(ForeignKey(f"{DbSchemaEnum.DND.value}.source.id"))
    # fields
    name: Mapped[str] = mapped_column(nullable=False)
    casting_time: Mapped[str] = mapped_column(nullable=False)
    classes = Column(MutableList.as_mutable(ARRAY(String)), nullable=False)
    components: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    duration: Mapped[str] = mapped_column(nullable=False)
    level: Mapped[int] = mapped_column(nullable=False)
    range: Mapped[str] = mapped_column(nullable=False)
    ritual: Mapped[bool] = mapped_column(nullable=False)
    school: Mapped[SpellSchoolEnum] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now(), nullable=False)
    created_by: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        index=True,
        default=func.now(),
        onupdate=datetime.datetime.now(datetime.UTC),
        nullable=False,
    )
    updated_by: Mapped[str] = mapped_column(nullable=False)
    homebrew: Mapped[bool] = mapped_column(default=True, nullable=False)
    # relationships
    source = relationship("Source")
    # constraints
    UniqueConstraint("source_id", "name", name="ux_spell")
