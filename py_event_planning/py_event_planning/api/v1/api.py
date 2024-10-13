"""FastAPI route definitions."""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from py_event_planning.features.auth.router import router as auth_router

# from py_event_planning.features.auth.service2 import get_auth
from py_event_planning.features.auth.service import get_auth
from py_event_planning.features.core.router import router as core_router
from py_event_planning.features.game_session.router import router as game_session_router

# global route collection
api_router = APIRouter(default_response_class=JSONResponse)

public_routes = APIRouter()
public_routes.include_router(core_router, prefix="", tags=[])
public_routes.include_router(auth_router, prefix="/auth", tags=["Auth"])

authenticated_routes = APIRouter()
authenticated_routes.include_router(game_session_router, prefix="/game-session", tags=["Game Session"])

api_router.include_router(public_routes)
api_router.include_router(authenticated_routes, dependencies=[Depends(get_auth)])
