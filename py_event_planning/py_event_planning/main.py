"""Main file for the py_event_planning API."""

# import sys
# from functools import lru_cache

import uvicorn

# from pydantic import BaseModel
# from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from py_event_planning.core.app import init_app
from py_event_planning.core.config import Settings, get_settings

settings: Settings = get_settings()

app = init_app(True)

origins = [
    "http://localhost:4200",  # local UI
    "http://localhost:8002",  # this API
    "http://127.0.0.1:8002",  # also this API
    "http://0.0.0.0:8002",  # also this API
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

if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
