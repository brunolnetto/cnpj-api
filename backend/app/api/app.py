# Description: This file initializes the FastAPI application and sets up configurations.

from fastapi import FastAPI, status, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.app.setup.config import settings
from backend.app.setup.logging import logger
from backend.app.api.routes.router_bundler import api_router
from backend.app.database.base import init_database
from backend.app.api.utils.ml import init_nltk


def custom_generate_unique_id(route: APIRoute) -> str:
    tag = "" if not route.tags else route.tags[0]
    name = route.name
    route_label = f"{tag}-{name}" if tag else name

    return route_label


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    init_nltk()
    yield


def create_app():
    # Generates the FastAPI application
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        summary=settings.DESCRIPTION,
        docs_url=f"{settings.API_V1_STR}/docs",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        generate_unique_id_function=custom_generate_unique_id,
        lifespan=lifespan,
    )

    return app_


def setup_app(app_):
    """
    Setup the application with the necessary configurations.

    Args:
        app_ (FastAPI): FastAPI application instance

    Returns:
        FastAPI: FastAPI application instance with the necessary configurations
    """

    # Add routers here
    app_.include_router(api_router, prefix=settings.API_V1_STR)

    # Add static files
    obj = StaticFiles(directory="static")
    app_.mount("/static", obj, name="static")

    # Add favicon
    @app_.get("/favicon.ico", include_in_schema=False)
    async def my_favicon():
        return FileResponse("static/favicon.ico")

    @app_.exception_handler(status.HTTP_404_NOT_FOUND)
    async def not_found_handler(request: Request, exc: HTTPException):
        warning_msg=f"The requested resource could not be found."
        suggestion_msg=f"Refer to the API documentation at {settings.API_V1_STR}/docs for available endpoints."
        return JSONResponse(
            f"{warning_msg} {suggestion_msg}",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    @app_.exception_handler(Exception)  # Catch all exceptions
    async def general_exception_handler(request: Request, exc: Exception):
        """Handles all uncaught exceptions."""
        # Log the exception details
        logger.error(f"Unhandled exception: {exc}")

        # Return a generic error response to the client
        code=status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(f"An unexpected error occurred: {exc}.", status_code=code)


    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app_.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip("/") 
                for origin in settings.BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    return app_


def init_app():
    # Get the number of applications from the environment variable
    app = create_app()

    # Setup the application
    app = setup_app(app)

    return app


# Initialize the application
app = init_app()
