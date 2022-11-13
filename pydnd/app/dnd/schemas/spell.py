"""Schemas for the spell table and its CRUD operations."""
from datetime import datetime
from typing import List, Optional

from dnd import schemas
from pydantic import BaseModel, Field


class SpellBase(BaseModel):
    """Schema base fields where everything is optional."""

    id: Optional[int] = Field(title="ID", description="Spell ID (generated)")
    source_id: Optional[int] = Field(title="Source ID", description="FK - Source ID")
    name: Optional[str] = Field(
        title="Name", description="Name of the spell (will be set to lowercase)"
    )
    casting_time: Optional[str] = Field(
        title="Casting Time", description="How long it takes to cast the spell"
    )
    classes: Optional[List[str]] = Field(
        default=[],
        title="Classes",
        description="List of classes that can cast the spell",
    )
    components: Optional[str] = Field(
        # TODO: ? default="v, s, m (some materials)",
        title="Components",
        description="v, s, m (materials to cast the spell)",
    )
    description: Optional[str] = Field(
        title="Description", description="Spell description in HTML format (sanatized)"
    )
    duration: Optional[str] = Field(
        title="Duration", description="How long the spell lasts"
    )
    level: Optional[int] = Field(
        title="Level",
        description="Spell level as an integer (0-9)",
        ge=0,  # >= 0
        le=9,  # <= 9
    )
    range: Optional[str] = Field(title="Range", description="The range of the spell")
    ritual: Optional[bool] = Field(
        title="Ritual", description="Can you cast the spell as a ritual"
    )
    school: Optional[schemas.SpellSchoolEnum] = Field(
        title="School", description="The school of magic of the spell"
    )
    created_at: Optional[datetime] = Field(
        title="School", description="[db] Timestamp of initial creation (generated)"
    )
    created_by: Optional[str] = Field(
        title="Created By", description="[db] Who created the spell"
    )
    updated_at: Optional[datetime] = Field(
        title="Created At", description="[db] Timestamp of last update (generated)"
    )
    updated_by: Optional[str] = Field(
        title="Updated By", description="[db] Who updated the spell"
    )
    homebrew: Optional[bool] = Field(
        title="Homebrew", description="Is the spell official content (generated)"
    )


class SpellCreate(SpellBase):
    """Schema for creation with required overrides and aditonal fields."""

    source_id: int = Field(title="Source ID", description="FK - Source ID")
    name: str = Field(
        title="Name", description="Name of the spell (will be set to lowercase)"
    )
    casting_time: str = Field(
        title="Casting Time", description="How long it takes to cast the spell"
    )
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
    description: str = Field(
        title="Description", description="Spell description in HTML format (sanatized)"
    )
    duration: str = Field(title="Duration", description="How long the spell lasts")
    level: int = Field(
        title="Level",
        description="Spell level as an integer (0-9)",
        ge=0,  # >= 0
        le=9,  # <= 9
    )
    range: str = Field(title="Range", description="The range of the spell")
    ritual: bool = Field(
        title="Ritual", description="Can you cast the spell as a ritual"
    )
    school: schemas.SpellSchoolEnum = Field(
        title="School", description="The school of magic of the spell"
    )
    created_by: str = Field(
        title="Created By", description="[db] Who created the spell"
    )
    updated_by: str = Field(
        title="Updated By", description="[db] Who updated the spell"
    )
    homebrew: bool = Field(
        title="Homebrew", description="Is the spell official content (generated)"
    )


class SpellUpdate(SpellBase):
    """Schema for updating model with required overrides and aditonal fields."""

    id: int = Field(title="ID", description="Spell ID (generated)")


class SpellResponse(SpellBase):
    """Schema for transforming ORM Model into a response object."""

    class Config:
        """Pydantic model configuration."""

        orm_mode = True
