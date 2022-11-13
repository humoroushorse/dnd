"""Base for CRUD repositories."""
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union

from dnd.database.base_class import Base
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class for CRUD repositories."""

    def __init__(self, model: Type[ModelType]):
        """Repository (CRUD) object with default methods to Create, Read, Update, Delete (Repository).

        Args:
            model (Type[ModelType]): A SQLAlchemy model class
        Returns:
            None
        """
        self.model = model

    def query(
        self,
        db: Session,
        params: Dict[str, Union[List[Any], str]],
        *,
        order_by: Optional[Any] = None,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0
    ) -> List[ModelType]:
        """Query a list of Type[ModelType] with filters.

        Args:
            db (Session): A SQLAlchemy Session.
            params (Dict[str, Union[List[Any], str]]): A dict of fields from Type[ModelType] to query.
            order_by (Optional[Any], optional): SQL 'ORDER BY' input. Defaults to None.
            limit (Optional[int], optional): SQL 'LIMIT'. Defaults to 100.
            offset (Optional[int], optional): SQL 'OFFSET'. Defaults to 0.

        Returns:
            List[ModelType]: A list of the inheriting classes' Type[ModelType].
        """
        models = db.query(self.model)
        if params:
            models = self.apply_param_filters_to_model(model=models, params=params)
        if order_by is not None:
            models = models.order_by(order_by)
        if offset:
            models = models.offset(offset)
        if limit:
            models = models.limit(limit)
        models = models.all()
        return models

    def get(self, db: Session, model_id: Any) -> Optional[ModelType]:
        """Get a single Type[ModelType].

        Args:
            db (Session): A SQLAlchemy Session.
            model_id (Any): the id of the Type[ModelType] to get by

        Returns:
            Optional[ModelType]: A single Type[ModelType] from the inheriting class.
        """
        return db.query(self.model).filter(self.model.id == model_id).one_or_none()

    def get_multi(
        self, db: Session, *, offset: int = 0, limit: int = 100
    ) -> Tuple[List[ModelType], int]:
        """Get a list of Type[ModelType] without filters.

        Args:
            db (Session): A SQLAlchemy Session.
            limit (Optional[int], optional): SQL 'LIMIT'. Defaults to 0.
            offset (Optional[int], optional): SQL 'OFFSET'. Defaults to 100.

        Returns:
            Tuple[List[ModelType], int]: A list of the inheriting classes' Type[ModelType].
        """
        models = db.query(self.model)
        total_count = models.count()
        models = models.offset(offset).limit(limit).all()
        return models, total_count

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new Type[CreateSchemaType].

        Args:
            db (Session): A SQLAlchemy Session.
            obj_in (CreateSchemaType): The model to be created.

        Returns:
            ModelType: The created Type[ModelType] from the inheriting class.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing Type[CreateSchemaType].

        Args:
            db (Session): A SQLAlchemy Session.
            db_obj (ModelType): The already existing object in the database.
            obj_in (CreateSchemaType): The new object used for updating the 'db_obj' input.

        Returns:
            ModelType: The updated Type[ModelType] from the inheriting class.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, model_id: int) -> ModelType:
        """Remove a Type[CreateSchemaType].

        Args:
            db (Session): A SQLAlchemy Session.
            model_id (int): The model's unique id.

        Returns:
            ModelType: The deleted Type[ModelType] from the inheriting class.
        """
        obj = db.query(self.model).get(model_id)
        db.delete(obj)
        db.commit()
        return obj

    def apply_param_filters_to_model(
        self,
        model: ModelType,
        params: Optional[Dict[str, Union[Any, List[Any]]]] = None,
    ) -> ModelType:
        """Takes a param dict and turns it into SQLAlchemy filters.

        Args:
            model (ModelType): The model to apply filters to.
            params (Optional[Dict[str, Union[Any, List[Any]]]], optional):
                A dict of filters based on the ModelType's fields. Defaults to None.

        Returns:
            ModelType: The model with the new filters applied.
        """
        if not params:
            return model
        filters = []
        for k, v in params.items():
            filters.extend(self._get_filter_list(k, v))
        model = model.filter(*filters)
        return model

    def _get_filter_list(
        self, key: str, value: Union[List[Any], Any, None], model: Optional[Any] = None
    ) -> List[Any]:
        """Gets filters based on the param's value type.

        Args:
            key (str): The param dict key.
            value (Union[List[Any], Any, None]): The param dict value.
            model (Optional[Any], optional): The model that will be filtered. Defaults to None.

        Returns:
            List[Any]: A list of filters.
        """
        key = str(key).split(".")[-1]
        if not model:
            model = self.model
        filters = []
        model_field: InstrumentedAttribute = getattr(model, key)
        if value:
            if isinstance(value, list):
                filters.append(model_field.in_(value))
            elif isinstance(value, int):
                filters.append(model_field == value)
            elif isinstance(value, Enum):
                filters.append(model_field == value)
            else:
                # TODO: should we use ilike?
                filters.append(model_field.like(str(value)))
        return filters
