"""Middleware that adds logging context and handles trace_id."""

import time
import uuid
from typing import Awaitable, Callable

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that adds request_id to logging, request, and response.

    Args:
        BaseHTTPMiddleware (_type_): _description_
    """

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """Middleware dispatch.

        Args:
            request (Request): _description_
            call_next (Callable[[Request], Awaitable[Response]]): _description_

        Returns:
            Response: _description_
        """
        # Create a request ID
        request_id = str(uuid.uuid4())

        # Add context to all loggers in all views
        with logger.contextualize(request_id=request_id):
            start_time = time.perf_counter()
            logger.trace("Start handling request: {} {}", request.method, request.url)
            request.state.request_id = request_id

            response: Response = await call_next(request)

            process_time = time.perf_counter() - start_time

            logger.trace(
                "Completed handling request: {} {} Status: {} Elapsed time: {} seconds",
                request.method,
                request.url,
                response.status_code,
                process_time,
            )

            response.headers.append("X-Request-ID", request_id)
            # response[] = request_id

            return response
