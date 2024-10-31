"""Game Session schemas."""

import datetime

from pydantic import BaseModel, ConfigDict, Field

from py_event_planning.features.game_system.schemas import GameSystemSchema
from py_event_planning.features.jt_user_game_session.schemas import JtUserGameSession
from py_event_planning.features.user.schemas import UserSchema
from py_event_planning.shared.schemas import (
    MixinBookeepingCreate,
    MixinBookeepingUpdate,
    MixinImageUrl,
    QueryBase,
)


class GameSessionSchema(BaseModel, MixinBookeepingCreate, MixinImageUrl):
    """How the game session shows up in the database."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        from_attributes=True,
    )

    # Fields of the model
    id: str = Field(title="Game Session ID")
    game_system_id: str = Field(title="Game System ID")
    game_system: GameSystemSchema | None = Field(default=None, title="Game System")
    jt_user_game_session: JtUserGameSession | None = Field(default=None, title="Join Table User/GameSession")
    game_master_id: str = Field(title="Game Master (User) ID")
    game_master: UserSchema | None = Field(default=None, title="Game Master (User)")
    title: str = Field(title="Title")
    description: str = Field(title="Description", min_length=3, max_length=360)
    start_date: datetime.datetime = Field(title="Start Date & Time")
    end_date: datetime.datetime = Field(title="End Date & Time")
    max_players: int | None = Field(default=6, title="Max Players", min=1)
    is_public: bool | None = Field(default=True, title="Is Public?")


class GameSessionCreate(BaseModel, MixinBookeepingCreate, MixinBookeepingUpdate, MixinImageUrl):
    """Allowed fields for creating a game session."""

    model_config = ConfigDict(extra="ignore", validate_assignment=True)
    # Fields of the model
    game_system_id: str = Field(title="Game System ID")
    game_master_id: str = Field(title="Game Master (User) ID")
    title: str = Field(title="Title")
    description: str = Field(title="Description", min_length=3, max_length=360)
    start_date: datetime.datetime = Field(title="Start Date & Time")
    end_date: datetime.datetime = Field(title="End Date & Time")
    max_players: int | None = Field(default=6, title="Max Players", min=1)
    is_public: bool | None = Field(default=True, title="Is Public?")


class GameSessionUpdate(BaseModel, MixinBookeepingUpdate, MixinImageUrl):
    """Allowed fields for editing a game session."""

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
    )

    # Fields of the model
    game_system_id: str = Field(title="Game System ID")
    game_master_id: str = Field(title="Game Master (User) ID")
    title: str = Field(title="Title")
    description: str = Field(title="Description", min_length=3, max_length=360)
    start_date: datetime.datetime = Field(title="Start Date & Time")
    end_date: datetime.datetime = Field(title="End Date & Time")
    max_players: int | None = Field(default=6, title="Max Players", min=1)
    is_public: bool | None = Field(default=True, title="Is Public?")


class GameSessionQuery(QueryBase):
    """Allowed fields for querying game sessions."""

    game_system_id: str | None = Field(default=None, title="Game System ID")
    game_master_id: str | None = Field(default=None, title="Game Master (User) ID")
    title: str | None = Field(default=None, title="Title")
    description: str | None = Field(
        default=None,
        title="Description Keyword(s)",
        description='Description keyword(s) to filter on (separated by commas ",")',
    )
