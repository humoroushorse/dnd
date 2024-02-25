"""FastAPI route definitions."""

from app.dnd.api.v1.endpoints import dnd_classes, jt_spells_to_classes, sources, spells
from fastapi import APIRouter

api_router = APIRouter()

# api_router.include_router(login.router, tags=["login"])
api_router.include_router(dnd_classes.router, prefix="/classes", tags=["classes"])
api_router.include_router(spells.router, prefix="/spells", tags=["spells"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(jt_spells_to_classes.router, prefix="/spell-to-class", tags=["spells", "classes"])
