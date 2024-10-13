"""init.

Revision ID: 82afae973ec2
Revises:
Create Date: 2024-09-17 21:52:20.138317

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

from py_dnd import shared

# revision identifiers, used by Alembic.
revision: str = "82afae973ec2"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade():
    """Database migration: upgrade."""
    pre_upgrade()

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "source",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("name_short", sa.String(), nullable=False),
        sa.Column("dnd_version", sa.String(), nullable=False),
        sa.Column("dnd_version_year", sa.Integer(), nullable=False),
        sa.Column("publish_year", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_source")),
        sa.UniqueConstraint("name", name=op.f("uq_source_name")),
        sa.UniqueConstraint("name_short", name=op.f("uq_source_name_short")),
        schema="dnd",
    )
    op.create_index(op.f("ix_dnd_source_id"), "source", ["id"], unique=False, schema="dnd")
    op.create_index(op.f("ix_dnd_source_updated_at"), "source", ["updated_at"], unique=False, schema="dnd")
    op.create_table(
        "spell",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("source_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("dnd_version", sa.String(), nullable=False),
        sa.Column("dnd_version_year", sa.Integer(), nullable=False),
        sa.Column("source_page", sa.Integer(), nullable=True),
        sa.Column(
            "level",
            sa.Enum(
                "CANTRIP",
                "FIRST",
                "SECOND",
                "THIRD",
                "FOURTH",
                "FIFTH",
                "SIXTH",
                "SEVENTH",
                "EIGHTH",
                "NINTH",
                name="spelllevelenum",
            ),
            nullable=False,
        ),
        sa.Column(
            "school",
            sa.Enum(
                "ABJURATION",
                "ALTERATION",
                "CONJURATION",
                "DIVINATION",
                "ENCHANTMENT",
                "EVOCATION",
                "TRANSMUTATION",
                "ILLUSION",
                "INVOCATION",
                "NECROMANCY",
                name="spellschoolenum",
            ),
            nullable=False,
        ),
        sa.Column("is_ritual", sa.Boolean(), nullable=False),
        sa.Column("casting_time", sa.String(), nullable=False),
        sa.Column("range", sa.String(), nullable=False),
        sa.Column("has_verbal_component", sa.Boolean(), nullable=False),
        sa.Column("has_somatic_component", sa.Boolean(), nullable=False),
        sa.Column("has_material_component", sa.Boolean(), nullable=False),
        sa.Column("materials", sa.String(), nullable=True),
        sa.Column("has_spell_cost", sa.Boolean(), nullable=False),
        sa.Column("are_materials_consumed", sa.Boolean(), nullable=False),
        sa.Column("duration", sa.String(), nullable=False),
        sa.Column("is_concentration", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("has_saving_throw", sa.Boolean(), nullable=False),
        sa.Column("difficulty_class_saving_throw_override", sa.Integer(), nullable=True),
        sa.Column("damage_type", sa.String(), nullable=True),
        sa.Column("at_higher_levels", sa.String(), nullable=True),
        sa.Column("difficulty_class_saving_throw", sa.String(), nullable=True),
        sa.Column("difficulty_class_type", sa.String(), nullable=True),
        sa.Column("stat_blocks", sa.JSON(), nullable=True),
        sa.Column("is_homebrew", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("updated_by", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["source_id"], ["dnd.source.id"], name=op.f("fk_spell_source_id_source")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_spell")),
        schema="dnd",
    )
    op.create_index(op.f("ix_dnd_spell_id"), "spell", ["id"], unique=False, schema="dnd")
    op.create_index(op.f("ix_dnd_spell_updated_at"), "spell", ["updated_at"], unique=False, schema="dnd")
    # ### end Alembic commands ###

    post_upgrade()


def downgrade():
    """Database migration: downgrade."""
    pre_downgrade()

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_dnd_spell_updated_at"), table_name="spell", schema="dnd")
    op.drop_index(op.f("ix_dnd_spell_id"), table_name="spell", schema="dnd")
    op.drop_table("spell", schema="dnd")
    op.drop_index(op.f("ix_dnd_source_updated_at"), table_name="source", schema="dnd")
    op.drop_index(op.f("ix_dnd_source_id"), table_name="source", schema="dnd")
    op.drop_table("source", schema="dnd")
    # ### end Alembic commands ###

    post_downgrade()


def pre_upgrade():
    # Processing before upgrading the schema
    op.execute(sa.text(f"CREATE SCHEMA IF NOT EXISTS {shared.enums.DbSchemaEnum.DND.value}"))


def post_upgrade():
    # Processing after upgrading the schema
    pass


def pre_downgrade():
    # Processing before downgrading the schema
    pass


def post_downgrade():
    # Processing after downgrading the schema
    sa.Enum(name="spelllevelenum").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="spellschoolenum").drop(op.get_bind(), checkfirst=False)
    # op.execute(sa.text(f"drop table {shared.enums.DbSchemaEnum.DND.value}.alembic_version"))
    # op.execute(sa.text(f"drop schema {shared.enums.DbSchemaEnum.DND.value}"))