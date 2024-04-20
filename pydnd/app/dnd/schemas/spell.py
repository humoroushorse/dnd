"""Schemas for the spell table and its CRUD operations."""

from datetime import datetime
from typing import List

from dnd import schemas
from pydantic import BaseModel, Field


class SpellBase(BaseModel):
    """Schema base fields where everything is optional."""

    id: int | None = Field(default=None, title="ID", description="Spell ID (generated)")
    source_id: int | None = Field(default=None, title="Source ID", description="FK - Source ID")
    name: str | None = Field(default=None, title="Name", description="Name of the spell (will be set to lowercase)")
    casting_time: str | None = Field(
        default=None, title="Casting Time", description="How long it takes to cast the spell"
    )
    classes: List[str] | None = Field(
        default=[],
        title="Classes",
        description="List of classes that can cast the spell",
    )
    components: str | None = Field(
        default=None,
        title="Components",
        description="v, s, m (materials to cast the spell)",
    )
    description: str | None = Field(
        default=None, title="Description", description="Spell description in HTML format (sanatized)"
    )
    duration: str | None = Field(default=None, title="Duration", description="How long the spell lasts")
    level: int | None = Field(
        default=None,
        title="Level",
        description="Spell level as an integer (0-9)",
        ge=0,  # >= 0
        le=9,  # <= 9
    )
    range: str | None = Field(default=None, title="Range", description="The range of the spell")
    ritual: bool | None = Field(default=None, title="Ritual", description="Can you cast the spell as a ritual")
    school: schemas.enums.SpellSchoolEnum | None = Field(
        default=None, title="School", description="The school of magic of the spell"
    )
    created_at: datetime | None = Field(
        default=None, title="School", description="[db] Timestamp of initial creation (generated)"
    )
    created_by: str | None = Field(default=None, title="Created By", description="[db] Who created the spell")
    updated_at: datetime | None = Field(
        default=None, title="Created At", description="[db] Timestamp of last update (generated)"
    )
    updated_by: str | None = Field(default=None, title="Updated By", description="[db] Who updated the spell")
    homebrew: bool | None = Field(
        default=None, title="Homebrew", description="Is the spell official content (generated)"
    )


class SpellCreate(SpellBase):
    """Schema for creation with required overrides and aditonal fields."""

    source_id: int = Field(title="Source ID", description="FK - Source ID")
    name: str = Field(title="Name", description="Name of the spell (will be set to lowercase)")
    casting_time: str = Field(title="Casting Time", description="How long it takes to cast the spell")
    classes: List[str] = Field(
        default=[],
        title="Classes",
        description="List of classes that can cast the spell",
    )
    components: str = Field(
        # TODO: ? default="v, s, m (some materials)",
        title="Components",
        description="v, s, m (materials to cast the spell)",
    )
    description: str = Field(title="Description", description="Spell description in HTML format (sanatized)")
    duration: str = Field(title="Duration", description="How long the spell lasts")
    level: int = Field(
        title="Level",
        description="Spell level as an integer (0-9)",
        ge=0,  # >= 0
        le=9,  # <= 9
    )
    range: str = Field(title="Range", description="The range of the spell")
    ritual: bool = Field(title="Ritual", description="Can you cast the spell as a ritual")
    school: schemas.enums.SpellSchoolEnum = Field(title="School", description="The school of magic of the spell")
    created_by: str = Field(title="Created By", description="[db] Who created the spell")
    updated_by: str = Field(title="Updated By", description="[db] Who updated the spell")
    homebrew: bool = Field(title="Homebrew", description="Is the spell official content (generated)")


class SpellUpdate(SpellBase):
    """Schema for updating model with required overrides and aditonal fields."""

    id: int = Field(title="ID", description="Spell ID (generated)")


class SpellResponse(SpellBase):
    """Schema for transforming ORM Model into a response object."""

    class Config:
        """Pydantic model configuration."""

        from_attributes = True
