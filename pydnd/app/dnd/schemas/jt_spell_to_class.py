"""Schemas for the jt_spell_to_class table and its CRUD operations."""

from typing import Optional

from pydantic import BaseModel, Field


class JtSpellToClassBase(BaseModel):
    """Schema base fields where everything is optional."""

    id: Optional[int] = Field(title="ID", description="JtSpellToClass ID (generated)")
    source_id: Optional[int] = Field(title="Source ID", description="FK - Source ID")
    dnd_class_id: Optional[int] = Field(title="Class ID", description="FK - Class ID")
    spell_id: Optional[int] = Field(title="Spell ID", description="FK - Spell ID")


class JtSpellToClassCreate(JtSpellToClassBase):
    """Schema for creation with required overrides and aditonal fields."""

    source_name: Optional[str] = Field(title="Source Name", description="FK - Source Name")
    dnd_class_name: Optional[str] = Field(title="Class Name", description="FK - Class Name")
    spell_name: Optional[str] = Field(title="Spell Name", description="FK - Spell Name")


class JtSpellToClassUpdate(JtSpellToClassBase):
    """Schema for updating model with required overrides and aditonal fields."""

    id: int = Field(title="ID", description="JtSpellToClass ID (generated)")
    source_name: Optional[str] = Field(title="Source Name", description="FK - Source Name")
    dnd_class_name: Optional[str] = Field(title="Class Name", description="FK - Class Name")
    spell_name: Optional[str] = Field(title="Spell Name", description="FK - Spell Name")


class JtSpellToClassResponse(JtSpellToClassBase):
    """Schema for transforming ORM Model into a response object."""

    class Config:
        """Pydantic model configuration."""

        orm_mode = True
