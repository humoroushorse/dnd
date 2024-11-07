"""Game Session route definitions."""

import asyncio
import datetime
from collections.abc import Hashable
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from loguru import logger
from pandas.core.series import Series

from py_event_planning.database.db import (
    AsyncMasterSessionDependency,
    AsyncReplicaSessionDependency,
)
from py_event_planning.features.auth.schemas import AuthUserToken
from py_event_planning.features.auth.service import UserAuth, UserAuthOptional
from py_event_planning.features.core.unit_of_work import (
    SqlAlchemyUnitOfWork,
    sqlalchemy_uow,
)
from py_event_planning.features.game_system.schemas import (
    GameSystemCreate,
    GameSystemCreateInput,
    GameSystemQuery,
    GameSystemSchema,
)
from py_event_planning.shared.schemas import BulkLoadResponse, GenericListResponse

router = APIRouter()


@router.get("")
async def read_game_systems(
    current_user: UserAuthOptional,
    db: AsyncReplicaSessionDependency,
    offset: int = 0,
    limit: int = 100,
) -> list[GameSystemSchema]:
    """Retrieve game_systems."""
    try:
        user = {}
        if current_user:
            user = {"sub": current_user.sub, "preferred_username": current_user.preferred_username}
        with logger.contextualize(user=user, log_threads=True):
            # user_logger = logger.bind(user_id=random.randint(0,99), user_username=random_name)
            async with sqlalchemy_uow(db, None) as uow:
                # entities = [entity async for entity in uow.game_session_repo.read_multi(offset=offset, limit=limit)]
                entities = await uow.game_system_repo.read_multi(offset=offset, limit=limit)
            return entities
    except HTTPException:
        # assume that the error was already logged
        raise
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error") from e


@router.get("/query")
async def query_game_systems(
    current_user: UserAuthOptional,
    db: AsyncReplicaSessionDependency,
    params: GameSystemQuery = Depends(),
) -> GenericListResponse[GameSystemSchema]:
    """Retrieve game_systems."""
    try:
        user = {}
        if current_user:
            user = {"sub": current_user.sub, "preferred_username": current_user.preferred_username}
        with logger.contextualize(user=user, log_threads=True):
            # user_logger = logger.bind(user_id=random.randint(0,99), user_username=random_name)
            filters = params.model_dump(exclude_none=True, exclude={"limit", "offset"})
            async with sqlalchemy_uow(db, None) as uow:
                entities, total_entities_count = await uow.game_system_repo.query(
                    params=filters, offset=params.offset, limit=params.limit
                )
            return GenericListResponse[GameSystemSchema](
                entities=entities,
                total_entities_count=total_entities_count,
                limit=params.limit,
                offset=params.offset,
                filters=filters,
            )
    except HTTPException:
        # assume that the error was already logged
        raise
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error") from e


async def upsert_and_mutate_report(
    uow: SqlAlchemyUnitOfWork,
    response: BulkLoadResponse,
    df_entity: tuple[Hashable, Series],
    name_index: int,
    current_user: AuthUserToken,
) -> None:
    """Adds a game_system and updates a bulk loading report.

    Args:
        uow (SqlAlchemyUnitOfWork): _description_
        response (BulkLoadResponse): _description_
        df_entity (tuple[Hashable, Series]): _description_
    """
    index, json_entity = df_entity
    entity: GameSystemCreate | None = None
    try:
        time_now = datetime.datetime.now(tz=datetime.UTC)
        entity = GameSystemCreate(
            **json_entity,
            created_at=time_now,
            created_by=current_user.sub,
            updated_at=time_now,
            updated_by=current_user.sub,
        )
        _, total_count = await uow.game_system_repo.query(params={"name": entity.name}, limit=1, exact=True)
        if total_count > 0:
            response.warnings.append(f"Game System with name '{entity.name}' already exists, skipping.")
        else:
            await uow.game_system_repo.create(model_in=entity, return_model=False)
            response.created.append(entity.name)
    except Exception as e:
        response.errors.append(f"row {index} [{entity.name if entity else json_entity.iloc[name_index]}]: {str(e)}")


@router.post("")
async def create_game_system(
    current_user: UserAuth,
    db: AsyncMasterSessionDependency,
    model_in: GameSystemCreateInput,
) -> GameSystemSchema:
    """Create game_system."""
    try:
        user = {"sub": current_user.sub, "preferred_username": current_user.preferred_username}
        with logger.contextualize(user=user, log_threads=True):
            async with sqlalchemy_uow(db, None) as uow:
                time_now = datetime.datetime.now(tz=datetime.UTC)
                model_create = GameSystemCreate(
                    **model_in.model_dump(),
                    created_at=time_now,
                    created_by=current_user.sub,
                    updated_at=time_now,
                    updated_by=current_user.sub,
                )
                entity = await uow.game_system_repo.create(model_in=model_create, return_model=True)
                await uow.commit()
            return entity
    except HTTPException:
        # assume that the error was already logged
        raise
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error") from e


@router.delete("/{entity_id}")
async def delete_game_system(
    current_user: UserAuth,
    db: AsyncMasterSessionDependency,
    entity_id: str,
) -> str:
    """Delete game_system."""
    try:
        user = {"sub": current_user.sub, "preferred_username": current_user.preferred_username}
        with logger.contextualize(game_system={id: entity_id}, user=user, log_threads=True):
            async with sqlalchemy_uow(db, None) as uow:

                delete_res = uow.game_system_repo.delete(entity_id=entity_id)
                if not delete_res:
                    logger.warning("Could not find entity to delete")
                    return entity_id
                await uow.commit()
                return str(entity_id)
    except HTTPException:
        # assume that the error was already logged
        raise
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error") from e


@router.post("/bulk")
async def bulk_create(
    *,
    current_user: UserAuth,
    db: AsyncMasterSessionDependency,
    file: UploadFile = File(description='Files of type: ["text/csv", "application/json"]'),
) -> BulkLoadResponse:
    """Bulk load in a list of game_system objects from a file.

    Supports file types: [application/json]
    """
    user = {"sub": current_user.sub, "preferred_username": current_user.preferred_username}
    with logger.contextualize(user=user, log_threads=True):
        try:
            allowed_file_types = ["text/csv", "application/json"]
            if file.content_type == "text/csv":
                contents = await file.read()
                df = pd.read_csv(BytesIO(contents))
            elif file.content_type == "application/json":
                contents = await file.read()
                df = pd.read_json(BytesIO(contents))
            else:
                # pylint: disable=W0707 (raise-missing-from)
                raise HTTPException(
                    400,
                    detail=(
                        f"Invalid document type. Expected on of: {[allowed_file_types]}"
                        + f", Received: {file.content_type}"
                    ),
                )

            response = BulkLoadResponse(filename=file.filename)
            async with sqlalchemy_uow(db, None) as uow:
                tasks = [
                    upsert_and_mutate_report(uow, response, entity, [*df.keys()].index("name"), current_user)
                    for entity in df.iterrows()
                ]
                await asyncio.gather(*tasks)

                if not response.errors:
                    await uow.db_session.flush()
                    await uow.commit()

            response.update_totals()
            return response
        except HTTPException:
            # assume that the error was already logged
            raise
        except Exception as e:
            logger.error("Uncaught error: {}", str(e))
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error") from e
