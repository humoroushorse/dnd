"""Game System schemas."""

from pydantic import UUID4, BaseModel, ConfigDict, Field

from py_event_planning.shared.schemas import (
    MixinBookeepingCreate,
    MixinBookeepingUpdate,
    QueryBase,
)


class GameSystemSchemaBase(BaseModel, MixinBookeepingCreate, MixinBookeepingUpdate):
    """How the game system shows up in the database."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        from_attributes=True,
        str_strip_whitespace=True,
    )
    id: UUID4 = Field(title="Game System ID")
    name: str = Field(title="Name")
    version: str = Field(title="Version")
    release_year: int = Field(title="Release Year")
    description: str = Field(title="Description")


class GameSystemSchema(GameSystemSchemaBase):
    """How the game system shows up in the database."""


class GameSystemCreateInput(BaseModel):
    """Fields used to create a game system (no generated fields)."""

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
    )
    name: str = Field(title="Name")
    version: str = Field(title="Version")
    release_year: int = Field(title="Release Year")
    description: str = Field(title="Description")


class GameSystemCreate(GameSystemCreateInput, MixinBookeepingCreate, MixinBookeepingUpdate):
    """Fields used to create a game system (with generated fields)."""


class GameSystemUpdateInput(BaseModel):
    """Fields you can update for a game system (no generated fields)."""

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
    )
    name: str = Field(title="Name")
    version: str = Field(title="Version")
    release_year: int = Field(title="Release Year")
    description: str = Field(title="Description")


class GameSystemUpdate(GameSystemUpdateInput, MixinBookeepingUpdate):
    """Fields you can update for a game system (with generated fields)."""


class GameSystemQuery(QueryBase):
    """Fields you can use to query game system(s)."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )
    name: str | None = Field(default=None, title="Name")
    version: str | None = Field(default=None, title="Version")
    release_year: int | None = Field(default=None, title="Release Year")
    description: str | None = Field(default=None, title="Description")
