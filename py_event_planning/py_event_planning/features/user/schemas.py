"""User schemas."""

import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator

from py_event_planning.shared.schemas import QueryBase


class UserSchemaBase(BaseModel):
    """How the User shows up in the database."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        from_attributes=True,
        str_strip_whitespace=True,
    )

    # Fields of the model
    id: uuid.UUID = Field(title="User ID")
    username: str | None = Field(default=None, title="Username")
    profile_picture_url: str | None = Field(default=None, title="Profile Picture URL")


class UserSchema(UserSchemaBase):
    """How the User shows up in the database (with relationships)."""


class UserCreate(BaseModel):
    """Fields used to create a user."""

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
    )
    id: uuid.UUID = Field(title="User ID")
    username: str | None = Field(default=None, title="Username")
    profile_picture_url: str | None = Field(default=None, title="Profile Picture URL")

    @field_validator("id")
    @classmethod
    def validate_uuid(cls, v: uuid.UUID | str) -> uuid.UUID:
        """Force inputs to uuid.UUID."""
        if isinstance(v, str):
            return uuid.UUID(v)
        return v

    # @field_serializer('id')
    # def serialize_uuid(self, v: uuid.UUID) -> str:
    #     return str(v)


class UserUpdate(BaseModel):
    """Fields you can update for a user."""

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    username: str | None = Field(default=None, title="Username")
    profile_picture_url: str | None = Field(default=None, title="Profile Picture URL")


class UserQuery(QueryBase):
    """Fields you can use to query user(s)."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )
    username: str | None = Field(default=None, title="Username")
    profile_picture_url: str | None = Field(default=None, title="Profile Picture URL")
