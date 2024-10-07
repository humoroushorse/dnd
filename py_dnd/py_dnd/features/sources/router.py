"""Sources route definitions."""

import asyncio
import math
from collections.abc import Hashable
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from loguru import logger
from pandas.core.series import Series

from py_dnd.database.db import AsyncSessionDependency
from py_dnd.features.core.unit_of_work import SqlAlchemyUnitOfWork, sqlalchemy_uow
from py_dnd.features.sources.schemas import SourceCreate, SourceQuery, SourceSchema
from py_dnd.shared.schemas import BulkLoadResponse, GenericListResponse

router = APIRouter()


@router.get("/query")
async def query_sources(
    db: AsyncSessionDependency,
    params: SourceQuery = Depends(),
) -> GenericListResponse[SourceSchema]:
    """Retrieve sources."""
    try:
        with logger.contextualize(user_id=123, user_username="Some User", log_threads=True):
            # user_logger = logger.bind(user_id=random.randint(0,99), user_username=random_name)
            filters = params.model_dump(exclude_none=True, exclude={"limit", "offset"})
            async with sqlalchemy_uow(db, None) as uow:
                entities, total_entities_count = await uow.source_repo.query(
                    params=filters, offset=params.offset, limit=params.limit
                )
            return GenericListResponse[SourceSchema](
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
    uow: SqlAlchemyUnitOfWork, response: BulkLoadResponse, df_entity: tuple[Hashable, Series]
) -> None:
    """Adds a source and updates a bulk loading report.

    Args:
        uow (SqlAlchemyUnitOfWork): _description_
        response (BulkLoadResponse): _description_
        df_entity (tuple[Hashable, Series]): _description_
    """
    index, entity = df_entity
    source = None
    try:
        if math.isnan(entity.get("publish_year")):
            entity["publish_year"] = None
        logger.info("ik -- index={}, entity=\n{}", index, entity)
        source = SourceCreate(**entity)
        _, total_count = await uow.source_repo.query(params={"name": source.name}, limit=1)
        if total_count > 0:
            response.warnings.append(f"Source with name '{source.name}' already exists, skipping.")
        else:
            await uow.source_repo.create(model_in=source, return_model=False)
            response.created.append(source.name)
    except Exception as e:
        response.errors.append(f"row {index} [{source.name if source else entity[2]}]: {str(e)}")


@router.post("/bulk")
async def bulk_create(
    *,
    db: AsyncSessionDependency,
    file: UploadFile = File(description='Files of type: ["text/csv", "application/json"]'),
) -> BulkLoadResponse:
    """Bulk load in a list of source objects from a file.

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
            tasks = [upsert_and_mutate_report(uow, response, entity) for entity in df.iterrows()]
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
