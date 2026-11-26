from fastapi import status, Request, HTTPException
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from backend.app.setup.config import settings
from backend.app.setup.logging import logger


# Detail Starlette uses when no route matches the requested path
ROUTE_NOT_FOUND_DETAIL = "Not Found"


async def not_found_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handles 404 Not Found exceptions.

    A 404 raised by an endpoint keeps its own detail. Only unknown routes get
    the generic message pointing to the API documentation.
    """
    detail = getattr(exc, "detail", None)
    headers = getattr(exc, "headers", None)

    if detail and detail != ROUTE_NOT_FOUND_DETAIL:
        return JSONResponse(
            content={"error_code": "RESOURCE_NOT_FOUND", "detail": detail},
            status_code=status.HTTP_404_NOT_FOUND,
            headers=headers,
        )

    warning_msg = "The requested resource could not be found."
    endpoints = f"{settings.API_V1_STR}/docs or {settings.API_V1_STR}/redoc"
    suggestion_msg = f"Refer to the API documentation on endpoints {endpoints}."

    return JSONResponse(
        content={
            "error_code": "RESOURCE_NOT_FOUND",
            "detail": warning_msg,
            "suggestion": suggestion_msg,
        },
        status_code=status.HTTP_404_NOT_FOUND,
        headers=headers,
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handles all uncaught exceptions."""
    logger.error(
        f"Unhandled exception occurred at {request.method} {request.url}: {exc}"
    )

    return JSONResponse(
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "detail": "An unexpected error occurred. Please try again later.",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def custom_rate_limit_handler(
    request: Request, exc: RateLimitExceeded
) -> JSONResponse:
    """Handles rate limit exceeded exceptions."""
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error_code": "RATE_LIMIT_EXCEEDED",
            "detail": "Too many requests, please slow down!",
        },
    )
