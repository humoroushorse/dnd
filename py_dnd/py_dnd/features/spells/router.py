"""Spell route definitions."""

import asyncio
import math
from io import BytesIO
from typing import Hashable

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from loguru import logger
from pandas.core.series import Series

from py_dnd.database.db import AsyncSessionDependency
from py_dnd.features.core.unit_of_work import SqlAlchemyUnitOfWork, sqlalchemy_uow
from py_dnd.features.spells.schemas import SpellCreate, SpellQuery, SpellSchema
from py_dnd.shared.schemas import BulkLoadResponse, GenericListResponse

router = APIRouter()


@router.get("/")
async def read_spells(
    db: AsyncSessionDependency,
    offset: int = 0,
    limit: int = 100,
) -> list[SpellSchema]:
    """Retrieve spells."""
    try:
        with logger.contextualize(user_id=123, user_username="Some User", log_threads=True):
            # user_logger = logger.bind(user_id=random.randint(0,99), user_username=random_name)
            async with sqlalchemy_uow(db, None) as uow:
                entities = [entity async for entity in uow.spell_repo.read_multi(offset=offset, limit=limit)]
            return entities
    except HTTPException:
        # assume that the error was already logged
        raise
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error") from e


@router.get("/query")
async def query_spells(
    db: AsyncSessionDependency,
    params: SpellQuery = Depends(),
) -> GenericListResponse[SpellSchema]:
    """Retrieve spells."""
    try:
        with logger.contextualize(user_id=123, user_username="Some User", log_threads=True):
            # user_logger = logger.bind(user_id=random.randint(0,99), user_username=random_name)
            filters = params.model_dump(exclude_none=True, exclude={"limit", "offset"})
            async with sqlalchemy_uow(db, None) as uow:
                entities, total_entities_count = await uow.spell_repo.query(
                    params=filters, offset=params.offset, limit=params.limit
                )
            return GenericListResponse[SpellSchema](
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
    uow: SqlAlchemyUnitOfWork, response: BulkLoadResponse, df_entity: tuple[Hashable, Series], name_index: int
) -> None:
    """Adds a spell and updates a bulk loading report.

    Args:
        uow (SqlAlchemyUnitOfWork): _description_
        response (BulkLoadResponse): _description_
        df_entity (tuple[Hashable, Series]): _description_
    """
    index, json_entity = df_entity
    entity: SpellSchema | None = None
    try:
        if not json_entity.get("source_page") or math.isnan(json_entity.get("source_page")):
            json_entity["source_page"] = None
        if not json_entity.get("difficulty_class_saving_throw_override") or math.isnan(
            json_entity.get("difficulty_class_saving_throw_override")
        ):
            json_entity["difficulty_class_saving_throw_override"] = None
        else:
            json_entity["difficulty_class_saving_throw_override"] = int(
                json_entity.get("difficulty_class_saving_throw_override")
            )
        if json_entity.get("difficulty_class_saving_throw"):
            json_entity["difficulty_class_saving_throw"] = str(json_entity["difficulty_class_saving_throw"])
        # TODO: stat_blocks should be handled as a json object (list of stat blocks)
        json_entity["stat_blocks"] = None
        entity = SpellCreate(**json_entity)
        _, total_count = await uow.spell_repo.query(params={"name": entity.name}, limit=1, exact=True)
        if total_count > 0:
            response.warnings.append(f"Spell with name '{entity.name}' already exists, skipping.")
        else:
            await uow.spell_repo.create(model_in=entity, return_model=False)
            response.created.append(entity.name)
    except Exception as e:
        import traceback

        logger.error(traceback.format_exc())
        response.errors.append(f"row {index} [{entity.name if entity else json_entity.iloc[name_index]}]: {str(e)}")


@router.post("/")
async def create_spell(
    db: AsyncSessionDependency,
    model_in: SpellCreate = Depends(),
) -> SpellSchema:
    """Create spell."""
    try:
        with logger.contextualize(user_id=123, user_username="Some User", log_threads=True):
            async with sqlalchemy_uow(db, None) as uow:
                entity = await uow.spell_repo.create(model_in=model_in)
            return entity
    except HTTPException:
        # assume that the error was already logged
        raise
    except Exception as e:
        logger.error("Uncaught error: {}", str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error") from e


@router.post("/bulk")
async def bulk_create(
    *,
    db: AsyncSessionDependency,
    file: UploadFile = File(description='Files of type: ["text/csv", "application/json"]'),
) -> BulkLoadResponse:
    """Bulk load in a list of spell objects from a file.

    Supports file types: [application/json]
    """
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
                detail=f"Invalid document type. Expected on of: {[allowed_file_types]}, Received: {file.content_type}",
            )

        response = BulkLoadResponse(filename=file.filename)

        async with sqlalchemy_uow(db, None) as uow:
            tasks = [
                upsert_and_mutate_report(uow, response, entity, [*df.keys()].index("name")) for entity in df.iterrows()
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
