from fastapi import FastAPI, status, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from backend.app.setup.config import settings
from backend.app.setup.logging import logger

async def not_found_handler(request: Request, exc: HTTPException):
    warning_msg = "The requested resource could not be found."
    endpoints = f"{settings.API_V1_STR}/docs or {settings.API_V1_STR}/redoc"
    suggestion_msg = f"Refer to the API documentation on endpoints {endpoints} for available endpoints."
    return JSONResponse(
        f"{warning_msg} {suggestion_msg}",
        status_code=status.HTTP_404_NOT_FOUND,
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handles all uncaught exceptions."""
    # Log the exception details
    logger.error(f"Unhandled exception: {exc}")

    # Return a generic error response to the client
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse(f"An unexpected error occurred: {exc}.", status_code=code)
