"""Sources schemas."""

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, StrictInt

from py_dnd.shared.schemas import MixinBookeeping, QueryBase


class SourceSchema(BaseModel, MixinBookeeping):
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


class SourceCreate(SourceSchema):
    """Allowed fields for creating a source."""

    id: str = Field(
        title="Source ID",
        description="[Generated] Unique database ID For the Source table.",
        validation_alias=AliasChoices("id", "source_id", "sourceId"),
    )


class SourceUpdate(SourceSchema):
    """Allowed fields for editing a source."""

    id: str = Field(
        title="Source ID",
        description="[Generated] Unique database ID For the Source table.",
        validation_alias=AliasChoices("id", "source_id", "sourceId"),
    )


class SourceQuery(QueryBase):
    """Allowed fields for querying source."""

    name: str | None = Field(default=None, title="Names", description='Name(s) to filter on (separated by commas ",")')
