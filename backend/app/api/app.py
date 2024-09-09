# Description: This file initializes the FastAPI application and sets up
# configurations.
from contextlib import asynccontextmanager

from fastapi import FastAPI, status, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from datetime import datetime

from backend.app.setup.config import settings
from backend.app.utils.database import log_app_start
from backend.app.api.middlewares.logs import AsyncRequestLoggingMiddleware
from backend.app.api.routes.router_bundler import api_router
from backend.app.api.exceptions import (
    not_found_handler,
    general_exception_handler,
    custom_rate_limit_handler,
)
from backend.app.api.dependencies.logs import get_app_start_logs_repository
from backend.app.database.base import init_database, multi_database
from backend.app.api.utils.ml import init_nltk
from backend.app.scheduler.bundler import task_orchestrator

from backend.app.rate_limiter import limiter


def custom_generate_unique_id(route: APIRoute) -> str:
    tag = "" if not route.tags else route.tags[0]
    name = route.name
    route_label = f"{tag}-{name}" if tag else name

    return route_label


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    task_orchestrator.start()
    log_app_start()
    
    init_nltk()

    yield

    task_orchestrator.shutdown()
    multi_database.disconnect()


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


def setup_app(app_: FastAPI):
    """
    Setup the application with the necessary configurations.

    Args:
        app_ (FastAPI): FastAPI application instance

    Returns:
        FastAPI: FastAPI application instance with the necessary configurations
    """

    ##########################################################################
    # Routers
    ##########################################################################
    app_.include_router(api_router, prefix=settings.API_V1_STR)

    ##########################################################################
    # Middleware
    ##########################################################################
    app_.add_middleware(AsyncRequestLoggingMiddleware)

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        urls = [str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS]

        app_.add_middleware(
            CORSMiddleware,
            allow_origins=urls,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add static files
    obj = StaticFiles(directory="static")
    app_.mount("/static", obj, name="static")

    # Add favicon
    @app_.get("/favicon.ico")
    @limiter.limit(settings.DEFAULT_RATE_LIMIT)
    async def get_favicon(request: Request):
        return FileResponse("static/favicon.ico")

    ##########################################################################
    # Exception
    ##########################################################################
    # Add exception handlers
    # Register the rate limit exceeded handler
    app_.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)
    app_.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_handler)
    app_.add_exception_handler(Exception, general_exception_handler)


def init_app():
    # Get the number of applications from the environment variable
    app = create_app()

    # Setup the application
    setup_app(app)

    return app


# Initialize the application
app = init_app()
