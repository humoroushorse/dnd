"""Core repository classes/functions for building reposigtories."""

from __future__ import annotations

import uuid
from enum import Enum
from typing import Any, AsyncIterator, Generic, Sequence, TypeVar

import loguru
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import Result, Select, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute

from py_event_planning.database.base_class import EventPlanningSchemaBase
from py_event_planning.database.exceptions import handle_sqlalchemy_errors_decorator

ModelType = TypeVar("ModelType", bound=EventPlanningSchemaBase)
ModelSchemaType = TypeVar("ModelSchemaType", bound=BaseModel)
ModelSchemaBaseType = TypeVar("ModelSchemaBaseType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryBase(Generic[ModelType, ModelSchemaType, ModelSchemaBaseType, CreateSchemaType, UpdateSchemaType]):
    """Base repositiroy.

    Args:
        Generic (_type_): typings for repository.
    """

    def __init__(
        self,
        session: AsyncSession,
        model: type[ModelType],
        schema: type[ModelSchemaType],
        schema_base: type[ModelSchemaBaseType],
        logger: loguru.Logger | None = None,
    ):
        """RepositoryBase.

        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.session = session
        self.model = model
        self.schema = schema
        self.schema_base = schema_base
        self.logger = logger if logger else loguru.logger

    @handle_sqlalchemy_errors_decorator
    async def read_by_id(self, entity_id: int, as_model: bool = False) -> ModelSchemaType | ModelType | None:
        """Get an entity by id.

        Args:
            entity_id (int): _description_

        Returns:
            ModelSchemaType | None: _description_
        """
        stmt = select(self.model).where(self.model.id == entity_id)
        model: ModelType = await self.session.scalar(stmt.order_by(self.model.id))
        if as_model:
            return model
        return self.schema.model_validate(model)

    # async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
    #     stmt = select(self.model).where(self.model.id == id)
    #     result = await db.execute(stmt)
    #     return result.scalars().first()

    @handle_sqlalchemy_errors_decorator
    async def read_multi_by_ids(
        self,
        entity_ids: list[int],
    ) -> AsyncIterator[ModelType]:
        """Get multiple entities by ids.

        Args:
            entity_ids (list[int]): _description_

        Returns:
            AsyncIterator[ModelType]: _description_

        Yields:
            Iterator[AsyncIterator[ModelType]]: _description_
        """
        stmt = select(self.model).where(self.model.id.in_(entity_ids))
        stream = await self.session.stream_scalars(stmt.order_by(self.model.id))
        async for row in stream:
            yield row

    @handle_sqlalchemy_errors_decorator
    async def read_multi(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[ModelSchemaType]:
        # ) -> AsyncIterator[ModelType]:
        """Get multiple entities (pagination optional).

        Args:
            offset (int, optional): _description_. Defaults to 0.
            limit (int, optional): _description_. Defaults to 100.

        Returns:
            AsyncIterator[ModelType]: _description_

        Yields:
            Iterator[AsyncIterator[ModelType]]: _description_
        """
        self.logger.debug("RepositoryBase::read_multi() called with offset={}, limit={}", offset, limit)
        stmt = select(self.model).offset(offset).limit(limit)
        # stream = await self.session.stream_scalars(stmt.order_by(self.model.id))
        # async for row in stream:
        #     yield row
        res = await self.session.scalars(stmt.order_by(self.model.id))
        return [self.schema.model_validate(e) for e in res]

    # async def get_multi(self, db: AsyncSession, *, offset: int = 0, limit: int = 100) -> list[ModelType]:
    #     stmt = select(self.model).offset(offset).limit(limit)
    #     result = await db.execute(stmt)
    #     return result.scalars().all()

    @handle_sqlalchemy_errors_decorator
    async def create(self, *, model_in: CreateSchemaType, return_model: bool = True) -> ModelSchemaType | None:
        """Create an entity.

        Args:
            model_in (CreateSchemaType): _description_
            return_model (bool, optional): _description_. Defaults to True.

        Raises:
            RuntimeError: _description_

        Returns:
            ModelType: _description_
        """
        entity = self.model(**model_in.model_dump())
        self.session.add(entity)
        if return_model:
            await self.session.flush()
            # new = await self.read_by_id(entity.id)
            # if not new:
            #     raise RuntimeError()
            # Note: do not define relationships here or you get greenlit errors
            #   TODO: look into a better solution?
            return self.schema_base.model_validate(entity)
        return None

    # async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data)
    #     db.add(db_obj)
    #     await db.commit()
    #     await db.refresh(db_obj)
    #     return db_obj

    # async def update(
    #     self, session: AsyncSession, *, db_obj: ModelType, model_in: UpdateSchemaType | dict[str, Any]
    # ) -> None:
    #     self.notebook_id = notebook_id
    #     self.title = title
    #     self.content = content
    #     await self.session.flush()

    @handle_sqlalchemy_errors_decorator
    async def update(
        self,
        *,
        db_obj: ModelType | None = None,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelSchemaBaseType | None:
        """Update an existing entity.

        Args:
            db_obj (ModelType): _description_
            obj_in (UpdateSchemaType | dict[str, Any]): _description_

        Returns:
            ModelSchemaBaseType: _description_
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.session.add(db_obj)
        return self.schema_base.model_validate(db_obj)

    @handle_sqlalchemy_errors_decorator
    async def delete(
        self,
        entity_id: uuid.UUID | str | int,
    ) -> uuid.UUID | str | int | None:
        """Delete an entity.

        Args:
            entity (ModelType): _description_

        Returns:
            int: _description_
        """
        stmt = select(self.model).where(self.model.id == entity_id)
        model: ModelType = await self.session.scalar(stmt.order_by(self.model.id))
        if not model:
            return None
        await self.session.delete(model)
        # await self.session.flush()
        return entity_id

    # async def delete(self, db: AsyncSession, *, id: int) -> ModelType:
    #     obj = await self.get(db, id)
    #     db.delete(obj)
    #     await db.commit()
    #     return obj

    @handle_sqlalchemy_errors_decorator
    async def query(
        self,
        params: dict[str, list[Any] | str | None],
        *,
        order_by: Any | None = None,
        limit: int | None = 100,
        offset: int | None = 0,
        exact: bool = False,
    ) -> tuple[Sequence[ModelType], int]:
        """Query a list of Type[ModelType] with filters.

        Args:
            db (Session): A SQLAlchemy Session.
            params (dict[str, list[Any] | str | None]): A dict of fields from Type[ModelType] to query.
            order_by (Any, None, optional): SQL 'ORDER BY' input. Defaults to None.
            limit (int | None, optional): SQL 'LIMIT'. Defaults to 100.
            offset (int | None, optional): SQL 'OFFSET'. Defaults to 0.

        Returns:
            tuple[Sequence[ModelType], int]: A tuple of the entities and the total_count.
        """
        total_count: int | None = None
        query: Select = select(self.model)
        if params:
            query = self.apply_param_filters_to_query(query=query, params=params, exact=exact)
        # get count before limit/offset are applied
        if limit != 0 or offset != 0:
            query_count: Select = select(func.count()).select_from(query)
            query_count_result: Result = await self.session.execute(query_count)
            total_count = int(query_count_result.scalar_one())
        # apply limit/offset/order_by
        if order_by is not None:
            query = query.order_by(order_by)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        result: Result = await self.session.execute(query)
        # if no limit/offset assume count is lenght of result
        entities = [self.schema.model_validate(e) for e in result.scalars().all()]
        if total_count is None:
            self.logger.debug("No limit/offset set, assuming total_count = len(result)")
            total_count = len(entities)
        return entities, total_count

    def apply_param_filters_to_query(
        self, query: Select, params: dict[str, Any | list[Any]] | None = None, exact: bool = False
    ) -> ModelType:
        """Takes a param dict and turns it into SQLAlchemy filters.

        Args:
            query (Select): The query to apply filters to.
            params (dict[str, Any | list[Any]] | None, optional):
                A dict of filters based on the Select's fields. Defaults to None.

        Returns:
            Select: The query with the new filters applied.
        """
        if not params:
            return query
        filters = []
        for k, v in params.items():
            filters.extend(self._get_filter_list(key=k, value=v, exact=exact))
        query = query.filter(*filters)
        return query

    def _get_filter_list(
        self, key: str, value: list[Any] | Any | None, model: Any | None = None, exact: bool = False
    ) -> list[Any]:
        """Gets filters based on the param's value type.

        Args:
            key (str): The param dict key.
            value (list[Any] | Any | None, optional): The param dict value.
            model (Any | None, optional): The model that will be filtered. Defaults to None.

        Returns:
            list[Any]: A list of filters.
        """
        if not model:
            model = self.model
        key = str(key).split(".")[-1]
        filters = []
        model_field: InstrumentedAttribute = getattr(model, key)
        if value:
            if isinstance(value, str) and "," in value:
                value = value.split(",")
            if isinstance(value, list):
                conditions = [model_field.ilike(f"%{v}%") for v in value]
                list_query = or_(*conditions)
                filters.append(list_query)
                # filters.append(model_field.in_(value))
            elif isinstance(value, (int, Enum)):
                filters.append(model_field == value)
            elif isinstance(value, uuid.UUID):
                filters.append(model_field == value)
            else:
                if exact:
                    filters.append(model_field.like(f"{value}"))
                else:
                    filters.append(model_field.ilike(f"%{value}%"))
        return filters
