"""Game Session route definitions."""

import datetime
import uuid

from fastapi import APIRouter, HTTPException, status
from loguru import logger

from py_event_planning.database.db import AsyncMasterSessionDependency
from py_event_planning.features.auth.service import UserAuth
from py_event_planning.features.core.unit_of_work import sqlalchemy_uow
from py_event_planning.features.game_session.schemas import GameSessionSchema
from py_event_planning.features.jt_user_game_session.schemas import (
    JtUserGameSessionCreate,
    JtUserGameSessionCreateInput,
    JtUserGameSessionSchema,
    JtUserGameSessionSchemaBase,
)

router = APIRouter()


@router.post("/{game_session_id}/join-session")
async def join_game_session(
    current_user: UserAuth,
    db: AsyncMasterSessionDependency,
    model_in: JtUserGameSessionCreateInput,
    game_session_id: uuid.UUID,
) -> JtUserGameSessionSchemaBase:
    """Create Join Table User/GameSystem Record."""
    try:
        user = {"sub": current_user.sub, "preferred_username": current_user.preferred_username}
        with logger.contextualize(user=user, log_threads=True):
            async with sqlalchemy_uow(db, None) as uow:
                model_in.user_id = uuid.UUID(current_user.sub)
                time_now = datetime.datetime.now(tz=datetime.UTC)
                model_create = JtUserGameSessionCreate(
                    **model_in.model_dump(),
                    game_session_id=game_session_id,
                    created_at=time_now,
                    created_by=current_user.sub,
                    updated_at=time_now,
                    updated_by=current_user.sub,
                )
                game_session_entity: GameSessionSchema | None = await uow.game_session_repo.read_by_id(
                    entity_id=game_session_id
                )
                if not game_session_entity:
                    logger.error("Game session does not exist!")
                    raise HTTPException(status.HTTP_404_NOT_FOUND, "Game session does not exist!")
                jt_entities: list[JtUserGameSessionSchema]
                jt_entities, _ = await uow.jt_user_game_system_repo.query(params={"game_session_id": game_session_id})
                if len(jt_entities) >= (game_session_entity.max_players if game_session_entity.max_players else 0):
                    error_message = (
                        f"Game Session '{game_session_id}' is already at capacity!"
                        + f" (max {game_session_entity.max_players} players)"
                    )
                    logger.error(error_message)
                    raise HTTPException(status.HTTP_400_BAD_REQUEST, error_message)
                new_jt_user_game_session = await uow.jt_user_game_system_repo.create(
                    model_in=model_create, return_model=True
                )
                await uow.commit()
            return new_jt_user_game_session
    except HTTPException:
        # assume that the error was already logged
        raise
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error") from e


@router.post("/{game_session_id}/leave-session")
async def leave_game_session(
    current_user: UserAuth,
    db: AsyncMasterSessionDependency,
    model_in: JtUserGameSessionCreateInput,
    game_session_id: uuid.UUID,
) -> uuid.UUID:
    """Delete jt_user_game_system."""
    try:
        user = {"sub": current_user.sub, "preferred_username": current_user.preferred_username}
        with logger.contextualize(game_system={}, user=user, log_threads=True):
            async with sqlalchemy_uow(db, None) as uow:
                model_in.user_id = uuid.UUID(current_user.sub)
                logger.info("Leaving game session", extra={"game_session_id": str(game_session_id)})
                entities: list[JtUserGameSessionSchema]
                entities, _ = await uow.jt_user_game_system_repo.query(
                    params={"user_id": uuid.UUID(current_user.sub), "game_session_id": game_session_id}
                )
                entities_for_user = [e for e in entities if str(e.user_id) == str(model_in.user_id)]
                if not entities_for_user:
                    error_message = "Could not find game session to leave"
                    logger.error(error_message)
                    raise HTTPException(status.HTTP_404_NOT_FOUND, error_message)
                entity = entities_for_user[0]
                if str(entity.user_id) != str(current_user.sub):
                    error_message = "You do not have permissions to remove the user from the session!"
                    logger.error(error_message)
                    raise HTTPException(status.HTTP_403_FORBIDDEN, error_message)
                await uow.jt_user_game_system_repo.delete(entity_id=entity.id)
                await uow.commit()
                # for entity in entities_for_user:
                #     if str(entity.user_id) != str(current_user.sub):
                #         error_message = "You do not have permissions to remove the user from the session!"
                #         logger.error(error_message)
                #         raise HTTPException(status.HTTP_403_FORBIDDEN, error_message)
                #     await uow.jt_user_game_system_repo.delete(entity=entity)
                #     await uow.commit()
                return entity.id
    except HTTPException:
        # assume that the error was already logged
        raise
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error") from e
