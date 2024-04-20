"""API /classes endpoint."""

import json
from typing import Any, List

from dnd import repository, schemas
from dnd.api.deps import get_db
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "",
    response_model=schemas.responses.GenericListResponse[schemas.dnd_class.DndClassResponse],
)
def read_dnd_classes(db: Session = Depends(get_db), offset: int = 0, limit: int = 100) -> Any:
    """Retrieve all dnd_classes."""
    dnd_classes, total_count = repository.dnd_class.get_multi(db, offset=offset, limit=limit)
    return schemas.responses.GenericListResponse[schemas.dnd_class.DndClassResponse](
        total_count=total_count,
        limit=limit,
        offset=offset,
        data_count=len(dnd_classes),
        data=dnd_classes,
    )


@router.post("", response_model=schemas.dnd_class.DndClassResponse)
def create_dnd_class(*, db: Session = Depends(get_db), dnd_class_in: schemas.dnd_class.DndClassCreate) -> Any:
    """Create new dnd_classes."""
    dnd_class = repository.dnd_class.create(db, obj_in=dnd_class_in)
    return dnd_class


@router.put("", response_model=schemas.dnd_class.DndClassResponse)
def update_dnd_class(*, db: Session = Depends(get_db), dnd_class_in: schemas.dnd_class.DndClassUpdate) -> Any:
    """Update existing dnd_classes."""
    dnd_class = repository.dnd_class.get(db, model_id=dnd_class_in.id)
    if not dnd_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The dnd_class with this ID does not exist in the system.",
        )
    dnd_class = repository.dnd_class.update(db, db_obj=dnd_class, obj_in=dnd_class_in)
    return dnd_class


@router.delete("", response_model=schemas.responses.MessageResponse)
def delete_dnd_class(*, db: Session = Depends(get_db), id: int) -> Any:  # pylint: disable=redefined-builtin
    """Delete existing dnd_class."""
    dnd_class = repository.dnd_class.get(db, model_id=id)
    if not dnd_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The dnd_class with this ID does not exist in the system.",
        )
    repository.dnd_class.remove(db, model_id=dnd_class.id)
    return {"message": f"Item with ID = {id} deleted."}


@router.post("/bulk", response_model=schemas.responses.BulkLoadResponse)
def create_upload_file(
    *,
    db: Session = Depends(get_db),
    upload_file: UploadFile = File(description="Files of type: ['json']"),
) -> Any:
    """Bulk load in a list of dnd_class objects from a file.

    Supports file types: [application/json]
    """
    allowed_file_types = ["application/json"]
    if upload_file.content_type not in allowed_file_types:
        raise HTTPException(
            400,
            detail=f"Invalid document type. Expected: {allowed_file_types}, Received: {upload_file.content_type}",
        )
    response = schemas.responses.BulkLoadResponse(filename=upload_file.filename)
    json_data: List[dict] = json.load(upload_file.file)
    for jd in json_data:
        try:
            dnd_class = schemas.dnd_class.DndClassCreate(**jd)
            existing_dnd_class = repository.dnd_class.query(db, params={"name": dnd_class.name})
            if len(existing_dnd_class) > 0:
                response.warnings.append(f"Class with name '{dnd_class.name}' already exists, skipping.")
            else:
                repository.dnd_class.create(db, obj_in=dnd_class)
                response.created.append(dnd_class.name)
        except Exception as e:
            response.errors.append(f"[{jd.get('name')}]: {str(e)}")
    response.update_totals()
    return response.model_dump()
