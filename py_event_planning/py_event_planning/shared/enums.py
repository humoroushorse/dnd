"""Shared enums."""

from enum import Enum


class DbSchemaEnum(str, Enum):
    """Database Schema Options."""

    EVENT_PLANNING = "event_planning"
