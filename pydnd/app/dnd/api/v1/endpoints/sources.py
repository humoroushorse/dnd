"""API /sources endpoint."""

import json
from typing import Any, List

from dnd import repository, schemas
from dnd.api.deps import get_db
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "",
    response_model=schemas.responses.GenericListResponse[schemas.source.SourceResponse],
)
def read_sources(db: Session = Depends(get_db), offset: int = 0, limit: int = 100) -> Any:
    """Retrieve all sources."""
    sources, total_count = repository.source.get_multi(db, offset=offset, limit=limit)
    return schemas.responses.GenericListResponse[schemas.source.SourceResponse](
        total_count=total_count,
        limit=limit,
        offset=offset,
        data_count=len(sources),
        data=sources,
    )


@router.post("", response_model=schemas.source.SourceResponse)
def create_source(*, db: Session = Depends(get_db), source_in: schemas.source.SourceCreate) -> Any:
    """Create new sources."""
    source = repository.source.create(db, obj_in=source_in)
    return source


@router.put("", response_model=schemas.source.SourceResponse)
def update_source(*, db: Session = Depends(get_db), source_in: schemas.source.SourceUpdate) -> Any:
    """Update existing sources."""
    source = repository.source.get(db, model_id=source_in.id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The source with this ID does not exist in the system.",
        )
    source = repository.source.update(db, db_obj=source, obj_in=source_in)
    return source


@router.delete("", response_model=schemas.responses.MessageResponse)
def delete_source(*, db: Session = Depends(get_db), id: int) -> Any:  # pylint: disable=redefined-builtin
    """Delete existing source."""
    source = repository.source.get(db, model_id=id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The source with this ID does not exist in the system.",
        )
    repository.source.remove(db, model_id=source.id)
    return {"message": f"Source with ID = {id} deleted."}


@router.post("/bulk", response_model=schemas.responses.BulkLoadResponse)
def create_upload_file(
    *,
    db: Session = Depends(get_db),
    upload_file: UploadFile = File(description="Files of type: ['json']"),
) -> Any:
    """Bulk load in a list of source objects from a file.

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
            source = schemas.source.SourceCreate(**jd)
            existing_source = repository.source.query(db, params={"name": source.name})
            if len(existing_source) > 0:
                response.warnings.append(f"Source with name '{source.name}' already exists, skipping.")
            else:
                repository.source.create(db, obj_in=source)
                response.created.append(source.name)
        except Exception as e:
            response.errors.append(f"[{jd.get('name')}]: {str(e)}")
    response.update_totals()
    return response.dict()
