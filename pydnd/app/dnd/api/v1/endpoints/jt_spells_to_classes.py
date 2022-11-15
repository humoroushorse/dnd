"""API /spell-to-class endpoint."""
import json
from typing import Any, List

from dnd import repository, schemas
from dnd.api.deps import get_db
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "", response_model=schemas.GenericListResponse[schemas.JtSpellToClassResponse]
)
def read_jt_spells_to_classes(
    db: Session = Depends(get_db), offset: int = 0, limit: int = 100
) -> Any:
    """Retrieve all jt_spells_to_classes."""
    jt_spells_to_classes, total_count = repository.jt_spell_to_class.get_multi(
        db, offset=offset, limit=limit
    )
    return schemas.GenericListResponse[schemas.JtSpellToClassResponse](
        total_count=total_count,
        limit=limit,
        offset=offset,
        data_count=len(jt_spells_to_classes),
        data=jt_spells_to_classes,
    )


@router.post("", response_model=schemas.JtSpellToClassResponse)
def create_jt_spell_to_class(
    *, db: Session = Depends(get_db), jt_spell_to_class_in: schemas.JtSpellToClassCreate
) -> Any:
    """Create new jt_spells_to_classes."""
    if jt_spell_to_class_in.source_name:
        source = repository.source.query(
            db, params={"name": jt_spell_to_class_in.source_name}
        )
        if not source:
            raise HTTPException(
                404, f"Source with name '{jt_spell_to_class_in.source_name}' not found!"
            )
        jt_spell_to_class_in.source_id = source[0].id
    if jt_spell_to_class_in.dnd_class_name:
        dnd_class = repository.dnd_class.query(
            db, params={"name": jt_spell_to_class_in.dnd_class_name}
        )
        if not dnd_class:
            raise HTTPException(
                404,
                f"Class with name '{jt_spell_to_class_in.dnd_class_name}' not found!",
            )
        jt_spell_to_class_in.dnd_class_id = dnd_class[0].id
    if jt_spell_to_class_in.spell_name:
        spell = repository.spell.query(
            db, params={"name": jt_spell_to_class_in.spell_name}
        )
        if not spell:
            raise HTTPException(
                404, f"Spell with name '{jt_spell_to_class_in.spell_name}' not found!"
            )
        jt_spell_to_class_in.spell_id = spell[0].id

    jt_spell_to_class = repository.jt_spell_to_class.create(
        db, obj_in=schemas.JtSpellToClassBase(**jt_spell_to_class_in.dict())
    )
    return jt_spell_to_class


@router.put("", response_model=schemas.JtSpellToClassResponse)
def update_jt_spell_to_class(
    *, db: Session = Depends(get_db), jt_spell_to_class_in: schemas.JtSpellToClassUpdate
) -> Any:
    """Update existing jt_spells_to_classes."""
    jt_spell_to_class = repository.jt_spell_to_class.get(
        db, model_id=jt_spell_to_class_in.id
    )
    if not jt_spell_to_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The jt_spell_to_class with this ID does not exist in the system.",
        )
    jt_spell_to_class = repository.jt_spell_to_class.update(
        db, db_obj=jt_spell_to_class, obj_in=jt_spell_to_class_in
    )
    return jt_spell_to_class


@router.delete("", response_model=schemas.Message)
def delete_jt_spell_to_class(
    *, db: Session = Depends(get_db), id: int  # pylint: disable=redefined-builtin
) -> Any:
    """Delete existing jt_spell_to_class."""
    jt_spell_to_class = repository.jt_spell_to_class.get(db, model_id=id)
    if not jt_spell_to_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The jt_spell_to_class with this ID does not exist in the system.",
        )
    repository.jt_spell_to_class.remove(db, model_id=jt_spell_to_class.id)
    return {"message": f"JtSpellToClass with ID = {id} deleted."}


@router.post("/bulk")
def create_upload_file(  # noqa: C901 <- ignore code complexity (12 > 9)
    *,
    db: Session = Depends(get_db),
    upload_file: UploadFile = File(description="Files of type: ['json']"),
) -> Any:
    """Bulk load in a list of jt_spell_to_class objects from a file.

    Supports file types: [application/json]
    """
    allowed_file_types = ["application/json"]
    if upload_file.content_type not in allowed_file_types:
        raise HTTPException(
            400,
            detail=f"Invalid document type. Expected: {allowed_file_types}, Received: {upload_file.content_type}",
        )
    json_data: List[dict] = json.load(upload_file.file)
    created: List[str] = []
    warnings: List[str] = []
    errors: List[str] = []
    for jd in json_data:
        # jd_source_id = jd.get('source_id')
        jd_source_name = jd.get("source_name")
        # jd_class_id = jd.get('class_id')
        jd_class_name = jd.get("class_name")

        still_legal = True

        sources = repository.source.query(db, params={"name": jd_source_name})
        if len(sources) == 0:
            still_legal = False
            errors.append(f"Source with name '{jd_source_name}' not found!")
        else:
            source = sources[0]

        dnd_classes = repository.dnd_class.query(db, params={"name": jd_class_name})
        if len(dnd_classes) == 0:
            still_legal = False
            errors.append(f"Class with name '{jd_class_name}' not found!")
        else:
            dnd_class = dnd_classes[0]

        if still_legal:
            for _, jd_spell_list in jd.get("spells", {}).items():
                for jd_spell_name in jd_spell_list:
                    try:
                        spells_by_name = repository.spell.query(
                            db, params={"name": jd_spell_name, "source_id": source.id}
                        )
                        if len(spells_by_name) == 0:
                            errors.append(
                                f"Spell with name '{jd_spell_name}' not found! "
                                + "(class_id={dnd_class.id}, source_id={source.id}, level={jd_spell_level})"
                            )
                        else:
                            spell = spells_by_name[0]
                            existing_spells_to_classes = (
                                repository.jt_spell_to_class.query(
                                    db,
                                    params={
                                        "source_id": source.id,
                                        "dnd_class_id": dnd_class.id,
                                        "spell_id": spell.id,
                                    },
                                )
                            )
                            if len(existing_spells_to_classes) > 0:
                                warnings.append(
                                    f"Link source '{source.name}', "
                                    + "class '{dnd_class.name}' "
                                    + "spell '{spell.name}' "
                                    + "already exists, skipping."
                                )
                            else:
                                spell_to_class = schemas.JtSpellToClassCreate(
                                    dnd_class_id=dnd_class.id,
                                    source_id=source.id,
                                    spell_id=spell.id,
                                )
                                repository.jt_spell_to_class.create(
                                    db, obj_in=spell_to_class
                                )
                                created.append(
                                    f"Linked source '{source.name}', class '{dnd_class.name}' spell '{spell.name}'"
                                )
                    except Exception as e:
                        errors.append(f"[{jd.get('name')}]: {str(e)}")
    return {
        "filename": upload_file.filename,
        "totals": {
            "created": len(created),
            "errored": len(errors),
            "warning": len(warnings),
        },
        "created": created,
        "warnings": warnings,
        "errors": errors,
    }