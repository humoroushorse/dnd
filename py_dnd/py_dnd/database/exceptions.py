from functools import wraps

import sqlalchemy.exc
from fastapi import HTTPException, status
from loguru import logger


def handle_sqlalchemy_errors(e: Exception):
    if isinstance(e, sqlalchemy.exc.IntegrityError):
        logger.error("SQLAlchemy IntegretyError - {}", e.detail)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An integrity error occurred: Possible duplicate or constraint violation.",
        ) from e
    elif isinstance(e, sqlalchemy.exc.DataError):
        logger.error("SQLAlchemy DataError - {}", e.detail)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="A data error occurred: Invalid input data."
        ) from e
    elif isinstance(e, sqlalchemy.exc.OperationalError):
        logger.error("SQLAlchemy OperationalError - {}", e.detail)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database operational error occurred. Please try again later.",
        ) from e
    elif isinstance(e, sqlalchemy.exc.ProgrammingError):
        logger.error("SQLAlchemy ProgrammingError - {}", e.detail)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A programming error occurred (skill issue): Invalid database operation.",
        ) from e
    elif isinstance(e, sqlalchemy.exc.InvalidRequestError):
        logger.error("SQLAlchemy InvalidRequestError - {}", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request error: The request cannot be processed due to the current state of the system.",
        ) from e
    elif isinstance(e, sqlalchemy.exc.InterfaceError):
        logger.error("SQLAlchemy InterfaceError - {}", e.detail)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database interface error occurred: Connection issue or misconfiguration.",
        ) from e
    elif isinstance(e, sqlalchemy.exc.DatabaseError):
        logger.error("SQLAlchemy DatabaseError - {}", e.detail)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A general database error occurred. Please try again later.",
        ) from e
    elif isinstance(e, sqlalchemy.exc.InternalError):
        logger.error("SQLAlchemy InternalError - {}", e.detail)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal database error occurred. Please try again later.",
        ) from e
    elif isinstance(e, sqlalchemy.exc.NotSupportedError):
        logger.error("SQLAlchemy NotSupportedError - {}", e.detail)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A not supported error occurred: Unsupported database operation.",
        ) from e
    elif isinstance(e, sqlalchemy.exc.SQLAlchemyError):
        logger.error("SQLAlchemy SQLAlchemyError - {}", str(e))
        if "UNIQUE constraint failed" in str(e.orig):
            raise ValueError("Duplicate entry found") from e
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while processing the request.",
            ) from e
    # raise non-sqlalchemy errors
    else:
        raise e


def handle_sqlalchemy_errors_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            handle_sqlalchemy_errors(e)

    return wrapper
