"""py_dnd app declaration."""

import contextlib
from typing import AsyncGenerator

import fastapi
from fastapi.middleware.gzip import GZipMiddleware

from py_dnd.api.v1.api import api_router
from py_dnd.core.config import Settings, get_settings
from py_dnd.core.logging import init_logging
from py_dnd.database import db_init
from py_dnd.database.session import sessionmanager
from py_dnd.middleware.logging_middleware import LoggingMiddleware

# from fastapi.middleware.trustedhost import TrustedHostMiddleware


settings: Settings = get_settings()


@contextlib.asynccontextmanager
async def app_lifespan(_app: fastapi.FastAPI) -> AsyncGenerator:
    """Application lifespan."""
    # Startup
    await init_logging(settings)
    await db_init.init(settings)
    yield

    # Shutdown
    if sessionmanager.engine is not None:
        await sessionmanager.close()


def init_app(init_db: bool = True) -> fastapi.FastAPI:
    """Create FastAPI application."""
    lifespan = None

    if init_db:
        sessionmanager.init(str(settings.POSTGRES_DATABASE_URI))
        lifespan = app_lifespan

    server = fastapi.FastAPI(
        title=settings.API_NAME,
        docs_url=settings.SWAGGER_URL,
        redoc_url=settings.REDOC_URL,
        lifespan=lifespan,
        # terms_of_service="http://example.com/terms/",
        contact={
            "name": "Ian Kirkpatrick",
            # "url": "http://ian.kirkpatrick.com",
            "email": "thehumoroushorse@gmail.com",
        },
        license_info={
            "name": "GNU General Public License v3.0",
            "identifier": "GPL-3.0-only",
            "url": "https://www.gnu.org/licenses/gpl-3.0.html",
        },
    )

    # see ./middleware
    server.add_middleware(LoggingMiddleware)

    # server.add_middleware(
    #     TrustedHostMiddleware, allowed_hosts=["localhost:4200"]
    # )

    # see: https://www.starlette.io/middleware/#gzipmiddleware
    server.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=9)  # default 500  # 1-9

    server.include_router(api_router)

    return server
