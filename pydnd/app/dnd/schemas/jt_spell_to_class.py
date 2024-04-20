"""Schemas for the jt_spell_to_class table and its CRUD operations."""

from pydantic import BaseModel, Field


class JtSpellToClassBase(BaseModel):
    """Schema base fields where everything is optional."""

    id: int | None = Field(default=None, title="ID", description="JtSpellToClass ID (generated)")
    source_id: int | None = Field(default=None, title="Source ID", description="FK - Source ID")
    dnd_class_id: int | None = Field(default=None, title="Class ID", description="FK - Class ID")
    spell_id: int | None = Field(default=None, title="Spell ID", description="FK - Spell ID")


class JtSpellToClassCreate(JtSpellToClassBase):
    """Schema for creation with required overrides and aditonal fields."""

    source_name: str | None = Field(default=None, title="Source Name", description="FK - Source Name")
    dnd_class_name: str | None = Field(default=None, title="Class Name", description="FK - Class Name")
    spell_name: str | None = Field(default=None, title="Spell Name", description="FK - Spell Name")


class JtSpellToClassUpdate(JtSpellToClassBase):
    """Schema for updating model with required overrides and aditonal fields."""

    id: int = Field(title="ID", description="JtSpellToClass ID (generated)")
    source_name: str | None = Field(default=None, title="Source Name", description="FK - Source Name")
    dnd_class_name: str | None = Field(default=None, title="Class Name", description="FK - Class Name")
    spell_name: str | None = Field(default=None, title="Spell Name", description="FK - Spell Name")


class JtSpellToClassResponse(JtSpellToClassBase):
    """Schema for transforming ORM Model into a response object."""

    class Config:
        """Pydantic model configuration."""

        from_attributes = True
