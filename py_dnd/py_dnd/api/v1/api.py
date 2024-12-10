"""FastAPI route definitions."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from py_dnd.features.auth.router import router as auth_router
from py_dnd.features.core.router import router as core_router
from py_dnd.features.sources.router import router as source_router
from py_dnd.features.spells.router import router as spell_router
from py_dnd.features.user.router import router as user_router

# global route collection
api_router = APIRouter(default_response_class=JSONResponse)

public_routes = APIRouter()
public_routes.include_router(core_router, prefix="", tags=[])
public_routes.include_router(auth_router, prefix="/auth", tags=["Auth"])
public_routes.include_router(user_router, prefix="/user", tags=["User"])
public_routes.include_router(source_router, prefix="/source", tags=["Source"])
public_routes.include_router(spell_router, prefix="/spell", tags=["Spell"])

api_router.include_router(public_routes)
