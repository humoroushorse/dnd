"""Main file for the pydnd API."""
import uvicorn
from dnd import schemas
from dnd.api.v1.api import api_router
from dnd.core import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

origins = [
    "http://localhost:4200",  # local UI
    "http://localhost:8000",  # this API
    "http://127.0.0.1:8000",  # also this API
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


@app.get("/", response_model=schemas.HealthCheck, tags=["status"])
async def health_check() -> schemas.HealthCheck:
    """Root API endpoint used for health check."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
    }


app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
