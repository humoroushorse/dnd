"""SQLAlchemy Table: spell definition."""

from typing import Any

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from py_dnd import shared
from py_dnd.database.base_class import DndSchemaBase
from py_dnd.features.sources.models import Source
from py_dnd.shared.models import MixinBookeeping


class Spell(MixinBookeeping, DndSchemaBase):
    """SQLAlchemy spell model."""

    __tablename__ = "spell"

    # keys
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    source_id: Mapped[str] = mapped_column(ForeignKey(Source.id))
    # fields
    name: Mapped[str] = mapped_column(nullable=False)
    dnd_version: Mapped[str] = mapped_column(nullable=False)
    dnd_version_year: Mapped[int] = mapped_column(nullable=False)
    source_page: Mapped[int | None] = mapped_column(default=None, nullable=True)
    level: Mapped[shared.enums.SpellLevelEnum] = mapped_column(nullable=False)
    school: Mapped[shared.enums.SpellSchoolEnum] = mapped_column(nullable=False)
    is_ritual: Mapped[bool] = mapped_column(nullable=False)
    casting_time: Mapped[str] = mapped_column(nullable=False)
    range: Mapped[str] = mapped_column(nullable=False)
    has_verbal_component: Mapped[bool] = mapped_column(nullable=False)
    has_somatic_component: Mapped[bool] = mapped_column(nullable=False)
    has_material_component: Mapped[bool] = mapped_column(nullable=False)
    materials: Mapped[str | None] = mapped_column(default=None, nullable=True)
    has_spell_cost: Mapped[bool] = mapped_column(nullable=False)
    are_materials_consumed: Mapped[bool] = mapped_column(nullable=False)
    duration: Mapped[str] = mapped_column(nullable=False)
    is_concentration: Mapped[bool] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    has_saving_throw: Mapped[bool] = mapped_column(nullable=False)
    difficulty_class_saving_throw_override: Mapped[int | None] = mapped_column(default=None, nullable=True)
    damage_type: Mapped[str | None] = mapped_column(default=None, nullable=True)
    at_higher_levels: Mapped[str | None] = mapped_column(default=None, nullable=True)
    difficulty_class_saving_throw: Mapped[str | None] = mapped_column(default=None, nullable=True)
    difficulty_class_type: Mapped[str | None] = mapped_column(default=None, nullable=True)
    stat_blocks: Mapped[dict[str, Any] | None] = mapped_column(default=None)
    is_homebrew: Mapped[bool] = mapped_column(default=True, nullable=False)
    # relationships
    source = relationship(Source)
    # constraints
    UniqueConstraint("source_id", "name", name="ux_spell")
