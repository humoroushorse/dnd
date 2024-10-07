"""FastAPI route definitions."""

from fastapi import APIRouter

from py_event_planning.features.core.router import router as core_router
from py_event_planning.features.game_session.router import router as game_session_router

api_router = APIRouter()

api_router.include_router(core_router, prefix="", tags=[])
api_router.include_router(game_session_router, prefix="/game-session", tags=["Game Session"])
