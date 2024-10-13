"""FastAPI route definitions."""

from fastapi import APIRouter

from py_dnd.features.core.router import router as core_router
from py_dnd.features.sources.router import router as source_router
from py_dnd.features.spells.router import router as spell_router

api_router = APIRouter()

api_router.include_router(core_router, prefix="", tags=[])
api_router.include_router(spell_router, prefix="/spells", tags=["Spells"])
api_router.include_router(source_router, prefix="/sources", tags=["Sources"])
