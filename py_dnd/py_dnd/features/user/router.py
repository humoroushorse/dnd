"""User (DB) route definitions."""

import uuid

from fastapi import APIRouter, HTTPException, status
from loguru import logger

from py_dnd.database.db import (
    AsyncMasterSessionDependency,
    AsyncReplicaSessionDependency,
)
from py_dnd.features.auth.service import UserAuth, UserAuthOptional
from py_dnd.features.core.unit_of_work import sqlalchemy_uow
from py_dnd.features.user.schemas import UserSchema, UserUpdate

router = APIRouter()


@router.get("/{entity_id}")
async def read_users(
    entity_id: uuid.UUID,
    current_user: UserAuthOptional,
    db: AsyncReplicaSessionDependency,
    # offset: int = 0,
    # limit: int = 100,
) -> UserSchema | None:
    """Retrieve user."""
    try:
        user = {}
        if current_user:
            user = {"sub": current_user.sub, "preferred_username": current_user.preferred_username}
        with logger.contextualize(user=user, log_threads=True):
            logger.info("Fetching user id={}", entity_id)
            async with sqlalchemy_uow(db, None) as uow:
                entitity = await uow.user_repo.read_by_id(entity_id=entity_id)
            return entitity
    except HTTPException:
        # assume that the error was already logged
        raise
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error") from e


@router.put("/{entity_id}")
async def update_user(
    entity_id: uuid.UUID,
    current_user: UserAuth,
    db: AsyncMasterSessionDependency,
    obj_in: UserUpdate,
) -> UserSchema | None:
    """Udate user."""
    try:
        user = {"sub": current_user.sub, "preferred_username": current_user.preferred_username}
        with logger.contextualize(user=user, obj_in=obj_in.model_dump(), log_threads=True):
            async with sqlalchemy_uow(db, None) as uow:
                logger.info("Updating user")
                if str(current_user.sub) != str(entity_id):
                    error_message = f"You're not allowed to update user with id {entity_id}"
                    logger.error(error_message)
                    raise HTTPException(status.HTTP_403_FORBIDDEN, error_message)
                db_obj = await uow.user_repo.read_by_id(entity_id=entity_id, as_model=True)
                entity = await uow.user_repo.update(db_obj=db_obj, obj_in=obj_in)
                await uow.commit()
            return entity
    except HTTPException:
        # assume that the error was already logged
        raise
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error") from e
