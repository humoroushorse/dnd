"""API enum values."""

from enum import Enum


class DbSchemaEnum(str, Enum):
    """Database Schema Options."""

    DND = "dnd"


class SpellSchoolEnum(str, Enum):
    """Spell School Options."""

    ABJURATION = "abjuration"
    CONJURATION = "conjuration"
    DIVININATION = "divination"
    ENCHANTMENT = "enchantment"
    ILLUSION = "illusion"
    EVOCATION = "evocation"  # originally 'invocation'
    NECROMANCY = "necromancy"
    TRANSMUTATION = "transmutation"  # originally 'alteration'


class SpellLevelEnum(str, Enum):
    """Spell Level Options."""

    CANTRIP = 0
    FIRST_LEVEL = 1
    SECOND_LEVEL = 2
    THIRD_LEVEL = 3
    FOURTH_LEVEL = 4
    FITH_LEVEL = 5
    SIXTH_LEVEL = 6
    SEVENTH_LEVEL = 7
    EIGTH_LEVEL = 8
    NINETH_LEVEL = 9
