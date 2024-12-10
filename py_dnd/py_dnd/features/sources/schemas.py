"""Sources schemas."""

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, StrictInt

from py_dnd.shared.schemas import (
    MixinBookeepingCreate,
    MixinBookeepingUpdate,
    QueryBase,
)


class SourceSchemaBase(BaseModel, MixinBookeepingCreate, MixinBookeepingUpdate):
    """How the source shows up in the database."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        from_attributes=True,
    )

    # Fields of the model
    id: str = Field(
        title="Source ID",
        description="[Generated] Unique database ID For the Source table.",
        validation_alias=AliasChoices("id", "source_id", "sourceId"),
    )
    name: str = Field(title="Name", description="The name of the source.")
    name_short: str = Field(
        title="Short Name",
        description="A short identifier for the source",
    )
    publish_year: StrictInt | None = Field(default=None, title="D&D Source Release Year")
    dnd_version: str = Field(title="D&D Version", description="The version of Dungeons and Dragons.")
    dnd_version_year: int = Field(
        title="D&D Version Year", description="The year that the version of Dungeons and Dragons came out."
    )


class SourceSchema(SourceSchemaBase):
    """How the source shows up in the database (with relationships)."""


class SourceCreateInput(SourceSchema):
    """Allowed fields for creating a source."""

    id: str = Field(
        title="Source ID",
        description="[Generated] Unique database ID For the Source table.",
        validation_alias=AliasChoices("id", "source_id", "sourceId"),
    )
    name: str = Field(title="Name", description="The name of the source.")
    name_short: str = Field(
        title="Short Name",
        description="A short identifier for the source",
    )
    publish_year: StrictInt | None = Field(default=None, title="D&D Source Release Year")
    dnd_version: str = Field(title="D&D Version", description="The version of Dungeons and Dragons.")
    dnd_version_year: int = Field(
        title="D&D Version Year", description="The year that the version of Dungeons and Dragons came out."
    )


class SourceCreate(SourceCreateInput, MixinBookeepingCreate, MixinBookeepingUpdate):
    """Allowed fields for creating a source."""


class SourceUpdateInput(SourceSchema):
    """Allowed fields for editing a source."""

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
    )
    name: str = Field(title="Name", description="The name of the source.")
    name_short: str = Field(
        title="Short Name",
        description="A short identifier for the source",
    )
    publish_year: StrictInt | None = Field(default=None, title="D&D Source Release Year")
    dnd_version: str = Field(title="D&D Version", description="The version of Dungeons and Dragons.")
    dnd_version_year: int = Field(
        title="D&D Version Year", description="The year that the version of Dungeons and Dragons came out."
    )


class SourceUpdate(SourceUpdateInput, MixinBookeepingUpdate):
    """Allowed fields for editing a source."""


class SourceQuery(QueryBase):
    """Allowed fields for querying source."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    name: str | None = Field(default=None, title="Names", description='Name(s) to filter on (separated by commas ",")')
