"""API /spells endpoint."""
import json
from typing import Any, List, Optional

from dnd import repository, schemas
from dnd.api.deps import get_db
from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

router = APIRouter()


acid_splash = {
    "name": "acid splash",
    "source_id": 0,
    "casting_time": "1 action",
    "classes": [
        "sorcerer",
        "wizard",
        "fighter (eldritch knight)",
        "rogue (arcane trickster)",
    ],
    "components": "v, s",
    "description": """
    <p>
        You hurl a bubble of acid. Choose one creature within range,
        or choose two creatures within range that are within 5 feet of each other.
        A target must succeed on a Dexterity saving throw or take 1d6 acid damage.
    </p>
    <p>
        This spells damage increases by 1d6 when you reach 5th Level (2d6), 11th level (3d6) and 17th level (4d6).
    </p>
    """,
    "duration": "instantaneous",
    "level": 0,
    "range": "60 feet",
    "ritual": False,
    "school": "conjuration",
    "created_by": "Swagger",
    "updated_by": "Swagger",
}


@router.get("", response_model=schemas.GenericListResponse[schemas.SpellResponse])
def read_spells(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    level: Optional[List[int]] = Query(
        [], title="Levels", description="list of spell levels"
    ),
    school: Optional[List[schemas.SpellSchoolEnum]] = Query(
        [], title="Schools", description="list of spell schools"
    ),
    class_names: Optional[List[str]] = Query(
        [], title="Class Names", description="list of class names"
    ),
    ritual: Optional[bool] = None,
    source_names: Optional[List[str]] = Query(
        [], title="Source Names", description="list of source names"
    ),
) -> Any:
    """Retrieve all spells."""
    params = {"name": name, "level": level, "school": school, "ritual": ritual}
    spells, total_count = repository.spell.query_special(
        db,
        params=params,
        limit=limit,
        offset=offset,
        class_names=class_names,
        source_names=source_names,
    )
    return schemas.GenericListResponse[schemas.SpellResponse](
        total_count=total_count,
        limit=limit,
        offset=offset,
        data_count=len(spells),
        data=spells,
    )


@router.post("", response_model=schemas.SpellResponse)
def create_spell(
    *, db: Session = Depends(get_db), spell_in: schemas.SpellCreate
) -> Any:
    """Create new spells."""
    spell = repository.spell.create(db, obj_in=spell_in)
    return spell


@router.put("", response_model=schemas.SpellResponse)
def update_spell(
    *,
    db: Session = Depends(get_db),
    spell_in: schemas.SpellUpdate = Body(example={**acid_splash, "id": 0}),  # type: ignore[arg-type]
) -> Any:
    """Update existing spells."""
    spell = repository.spell.get(db, model_id=spell_in.id)
    if not spell:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The spell with this ID does not exist in the system.",
        )
    spell = repository.spell.update(db, db_obj=spell, obj_in=spell_in)
    return spell


@router.delete("", response_model=schemas.Message)
def delete_spell(
    *, db: Session = Depends(get_db), id: int  # pylint: disable=redefined-builtin
) -> Any:
    """Delete existing spell."""
    spell = repository.spell.get(db, model_id=id)
    if not spell:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The spell with this ID does not exist in the system.",
        )
    repository.spell.remove(db, model_id=spell.id)
    return {"message": f"Spell with ID = {id} deleted."}


@router.post("/bulk")
def create_upload_file(
    *,
    db: Session = Depends(get_db),
    upload_file: UploadFile = File(description="Files of type: ['json']"),
) -> Any:
    """Bulk load in a list of spell objects from a file.

    Supports file types: [application/json]
    """
    allowed_file_types = ["application/json"]
    if upload_file.content_type not in allowed_file_types:
        raise HTTPException(
            400,
            detail=f"Invalid document type. Expected: {allowed_file_types}, Received: {upload_file.content_type}",
        )
    json_data: List[dict] = json.load(upload_file.file)
    created = []
    warnings = []
    errors = []
    for jd in json_data:
        try:
            spell = schemas.SpellCreate(**jd)
            existing_spell = repository.spell.query(db, params={"name": spell.name})
            if len(existing_spell) > 0:
                warnings.append(
                    f"Spell with name '{spell.name}' already exists, skipping."
                )
            else:
                repository.spell.create(db, obj_in=spell)
                created.append(spell.name)
        except Exception as e:
            errors.append(
                {
                    "name": jd.get("name"),
                    "error": str(e),
                }
            )
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
