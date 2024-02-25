"""Main file for the pydnd API."""

import sys
from functools import lru_cache

import uvicorn
from app.dnd import schemas
from app.dnd.api.v1.api import api_router
from app.dnd.core import Settings, uncached_settings
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

app = FastAPI(title=uncached_settings.PROJECT_NAME)


@app.on_event("startup")
def startup() -> None:
    """Application startup routines."""
    log_level = uncached_settings.LOG_LEVEL
    logger.add(
        "logs/{time}.log",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        rotation="1 day",
        retention="10 days",
        level=log_level,
    )
    logger.debug("This is a debug log!")
    logger.info("This is a info log!")
    logger.success("This is a success log!")
    logger.warning("This is a warning log!")
    logger.error("This is a error log!")
    logger.critical("This is a critical log!")
    logger.exception("This is a exception log!")


origins = [
    "http://localhost:4200",  # local UI
    "http://localhost:8001",  # this API
    "http://127.0.0.1:8001",  # also this API
    "http://0.0.0.0:8001",  # also this API
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     errors = []
#     for error in exc.errors():
#         root_key = error.get("loc")[1]
#         error_message = f"Error with field '{root_key}': {error.get('msg')}"
#         if exc:
#             if isinstance(exec.body, str):
#                 provided_value = exc.body
#             else:
#                 provided_value = exc.body.get(root_key)
#             errors.append({
#                 "error_message": error_message,
#                 "provided_value": provided_value,
#             })
#         else:
#             errors.append({
#                 "error_message": error_message,
#                 "provided_value": exc,
#             })
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         # content=jsonable_encoder({"detail": exc.errors(), "Error": errors}),
#         content=jsonable_encoder({"detail": errors}),
#     )

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors(), "Error": "Name field is missing"}),
#     )

# Root of API (health check)


@lru_cache
def get_settings() -> Settings:
    """Cached settings to prevent reads."""
    return Settings()


@app.get("/", response_model=schemas.health_check.HealthCheck, tags=["status"])
async def health_check(
    settings: Settings = Depends(get_settings),
) -> schemas.health_check.HealthCheck:
    """Root API endpoint used for health check."""
    return schemas.health_check.HealthCheck(
        name=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        docs_url=f"{app.root_path}{app.docs_url}",
        python_version=sys.version,
    )


app.include_router(api_router, prefix=uncached_settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(app, host=uncached_settings.HOST, port=uncached_settings.PORT)
