"""User repository."""

from __future__ import annotations

import loguru
from sqlalchemy.ext.asyncio import AsyncSession

from py_event_planning.features.core.repository import RepositoryBase
from py_event_planning.features.user.models import User
from py_event_planning.features.user.schemas import UserCreate, UserSchema, UserUpdate


class UserRepository(RepositoryBase[User, UserSchema, UserCreate, UserUpdate]):
    """User Session Repository.

    Args:
        RepositoryBase (_type_): _description_
    """

    def __init__(self, session: AsyncSession, logger: loguru.Logger | None = None):
        super().__init__(session=session, model=User, schema=UserSchema)
        self.logger.trace("{} created!", self.__class__.__name__)
