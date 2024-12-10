"""Core routes outside of features."""

import sys
from typing import Literal

import fastapi

from py_dnd.core.config import Settings, get_settings
from py_dnd.features.core.schemas import AppBaseRouteSchema

router = fastapi.APIRouter()


@router.get("/", tags=["Status"])
async def app_base_route(
    request: fastapi.Request,
    settings: Settings = fastapi.Depends(get_settings),
) -> AppBaseRouteSchema:
    """Root API endpoint used for health check."""
    swagger_docs_url = f"{request.url.scheme}://{request.url.netloc}{settings.SWAGGER_URL}"
    redoc_docs_url = f"{request.url.scheme}://{request.url.netloc}{settings.REDOC_URL}"
    return AppBaseRouteSchema(
        name=settings.API_NAME,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        swagger_url=swagger_docs_url,
        redoc_url=redoc_docs_url,
        python_version=sys.version,
    )


@router.get("/health", tags=["Status"])
async def health_check_route() -> Literal["ok"]:
    """Root API endpoint used for health check."""
    return "ok"
