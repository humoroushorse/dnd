"""Game Session schemas."""

from pydantic import BaseModel, ConfigDict, Field

from py_event_planning.shared.schemas import MixinBookeeping, QueryBase


class GameEventSchema(BaseModel, MixinBookeeping):
    """How the game event shows up in the database."""

    # Settings for the model
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        from_attributes=True,
    )

    # Fields of the model
    id: str = Field(title="Game Event ID")
    name: str = Field(title="Name", min_length=3, max_length=360)
    description: str = Field(title="Description", min_length=3, max_length=360)
    organizer: str = Field(title="Organizer")


class GameEventCreate(GameEventSchema):
    """Allowed fields for creating a game event."""

    model_config = ConfigDict(extra="ignore", validate_assignment=True)


class GameEventUpdate(GameEventSchema):
    """Allowed fields for editing a game event."""

    id: str = Field(exclude=True)


class GameEventQuery(QueryBase):
    """Allowed fields for querying game events."""

    name: str | None = Field(default=None, title="Names", description='Name(s) to filter on (separated by commas ",")')
    description: str | None = Field(
        default=None,
        title="Description Keyword(s)",
        description='Description keyword(s) to filter on (separated by commas ",")',
    )
