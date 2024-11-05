"""FastAPI route definitions."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from py_event_planning.features.auth.router import router as auth_router
from py_event_planning.features.core.router import router as core_router
from py_event_planning.features.game_session.router import router as game_session_router
from py_event_planning.features.game_system.router import router as game_system_router
from py_event_planning.features.jt_user_game_session.router import (
    router as jt_user_game_session_router,
)

# global route collection
api_router = APIRouter(default_response_class=JSONResponse)

public_routes = APIRouter()
public_routes.include_router(core_router, prefix="", tags=[])
public_routes.include_router(auth_router, prefix="/auth", tags=["Auth"])
public_routes.include_router(jt_user_game_session_router, prefix="/game-session", tags=["Game Session", "User"])
public_routes.include_router(game_session_router, prefix="/game-session", tags=["Game Session"])
public_routes.include_router(game_system_router, prefix="/game-system", tags=["Game System"])

api_router.include_router(public_routes)
