"""Game Session schemas."""

import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator

from py_event_planning.features.game_system.schemas import GameSystemSchema
from py_event_planning.features.jt_user_game_session.schemas import (
    JtUserGameSessionSchema,
)
from py_event_planning.features.user.schemas import UserSchema
from py_event_planning.shared.schemas import (
    MixinBookeepingCreate,
    MixinBookeepingUpdate,
    MixinImageUrl,
    QueryBase,
)


class GameSessionSchemaBase(BaseModel, MixinBookeepingCreate, MixinBookeepingUpdate, MixinImageUrl):
    """How the game session shows up in the database (no relationships)."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        from_attributes=True,
        str_strip_whitespace=True,
    )

    # Fields of the model
    id: uuid.UUID = Field(title="Game Session ID")
    game_system_id: uuid.UUID = Field(title="Game System ID")
    game_master_id: uuid.UUID = Field(title="Game Master (User) ID")
    title: str = Field(title="Title")
    description: str = Field(title="Description", min_length=3, max_length=360)
    start_date: datetime.datetime = Field(title="Start Date & Time")
    end_date: datetime.datetime = Field(title="End Date & Time")
    max_players: int | None = Field(default=6, title="Max Players", min=1)
    is_public: bool | None = Field(default=True, title="Is Public?")


class GameSessionSchema(GameSessionSchemaBase):
    """How the game session shows up in the database (with relationships)."""

    game_system: GameSystemSchema | None = Field(default=None, title="Game System")
    jt_user_game_session: list[JtUserGameSessionSchema] | None = Field(
        default=None, title="Join Table User/GameSession"
    )
    game_master: UserSchema | None = Field(default=None, title="Game Master (User)")


class GameSessionCreateInput(BaseModel, MixinImageUrl):
    """Fields used to create a game session (no generated fields)."""

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
    )
    # Fields of the model
    game_system_id: uuid.UUID = Field(title="Game System ID")
    game_master_id: uuid.UUID = Field(title="Game Master (User) ID")
    title: str = Field(title="Title")
    description: str = Field(title="Description", min_length=3, max_length=360)
    start_date: datetime.datetime = Field(title="Start Date & Time")
    end_date: datetime.datetime = Field(title="End Date & Time")
    max_players: int | None = Field(default=6, title="Max Players", min=1)
    is_public: bool | None = Field(default=True, title="Is Public?")

    @field_validator("start_date", "end_date")
    @classmethod
    def remove_tz_info_frorm_dates(cls, v: datetime.datetime) -> datetime.datetime:
        """Force UTC and replace with no TZ info."""
        dt = v.astimezone(datetime.timezone.utc)
        return dt.replace(tzinfo=None)


class GameSessionCreate(GameSessionCreateInput, MixinBookeepingCreate, MixinBookeepingUpdate):
    """Allowed fields for creating a game session."""


class GameSessionUpdate(BaseModel, MixinBookeepingUpdate, MixinImageUrl):
    """Allowed fields for editing a game session."""

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    # Fields of the model
    game_system_id: uuid.UUID = Field(title="Game System ID")
    game_master_id: uuid.UUID = Field(title="Game Master (User) ID")
    title: str = Field(title="Title")
    description: str = Field(title="Description", min_length=3, max_length=360)
    start_date: datetime.datetime = Field(title="Start Date & Time")
    end_date: datetime.datetime = Field(title="End Date & Time")
    max_players: int | None = Field(default=6, title="Max Players", min=1)
    is_public: bool | None = Field(default=True, title="Is Public?")


class GameSessionQuery(QueryBase):
    """Allowed fields for querying game sessions."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    game_system_id: uuid.UUID | None = Field(default=None, title="Game System ID")
    game_master_id: uuid.UUID | None = Field(default=None, title="Game Master (User) ID")
    title: str | None = Field(default=None, title="Title")
    description: str | None = Field(
        default=None,
        title="Description Keyword(s)",
        description='Description keyword(s) to filter on (separated by commas ",")',
    )
