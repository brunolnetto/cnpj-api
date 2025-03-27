# Description: This file initializes the FastAPI application and sets up various configurations,
# including middleware, CORS, static file serving, exception handlers, and rate limiting.
# It also defines the application's lifespan, which includes startup and shutdown tasks,
# and initializes the main application instance.
# configurations.
from contextlib import asynccontextmanager
from time import perf_counter
import asyncio
from functools import partial

from fastapi import FastAPI
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from backend.app.api.dependencies.cnpj import initialize_CNPJRepository
from backend.app.api.dependencies.logs import log_app_start
from backend.app.api.exceptions import general_exception_handler
from backend.app.api.exceptions import not_found_handler
from backend.app.api.middlewares.logs import (
    AsyncRequestLoggingMiddleware as ARLMiddleware,
)
from backend.app.api.middlewares.misc import TimingMiddleware
from backend.app.api.rate_limiter import limiter
from backend.app.api.routes.router_bundler import api_router
from backend.app.api.utils.misc import print_execution_time
from backend.app.api.utils.misc import execute_task_with_timing
from backend.app.api.utils.misc import execute_tasks_with_timing
from backend.app.api.utils.ml import init_nltk
from backend.app.database.base import init_database
from backend.app.database.base import multi_database
from backend.app.scheduler.bundler import add_tasks
from backend.app.scheduler.bundler import task_orchestrator
from backend.app.setup.config import settings
from backend.app.setup.logging import setup_logger

@asynccontextmanager
async def lifespan(app_: FastAPI):
    """Async context manager that handles startup and shutdown tasks."""
    
    # Define startup and shutdown tasks
    startup_tasks = [
        init_database, setup_logger, initialize_CNPJRepository,
        log_app_start, task_orchestrator.start, add_tasks, init_nltk
    ]
    shutdown_tasks = [
        task_orchestrator.shutdown, multi_database.disconnect
    ]

    # Run startup tasks
    await execute_tasks_with_timing(startup_tasks, "starting")

    try:
        yield  # Hand control over to FastAPI runtime
    finally:
        # Run shutdown tasks
        await execute_tasks_with_timing(shutdown_tasks, "shutting down")

def create_app():
    # Generates the FastAPI application
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        summary=settings.DESCRIPTION,
        docs_url=f"{settings.API_V1_STR}/docs",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan,
    )

    return app_


def setup_cors(app_: FastAPI) -> None:
    """Sets up CORS middleware for the application."""
    if settings.BACKEND_CORS_ORIGINS:
        urls = [str(origin).strip("/")
                for origin in settings.BACKEND_CORS_ORIGINS]
        app_.add_middleware(
            CORSMiddleware,
            allow_origins=urls,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def setup_middlewares(app_: FastAPI) -> None:
    """Adds middleware to the FastAPI application."""
    app_.add_middleware(ARLMiddleware)
    app_.add_middleware(GZipMiddleware, minimum_size=1000)
    app_.add_middleware(TimingMiddleware)
    app_.add_middleware(SlowAPIMiddleware)


def setup_static_files(app_: FastAPI) -> None:
    """Sets up static file serving for the FastAPI application."""
    directory_str = "static"
    statis_files = StaticFiles(directory=directory_str)
    app_.mount("/static", statis_files, name=directory_str)


def setup_exception_handlers(app_: FastAPI) -> None:
    async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests, please slow down!!"},
        )
    
    """Sets up exception handlers for the FastAPI application."""
    app_.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)
    app_.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_handler)
    app_.add_exception_handler(Exception, general_exception_handler)


def setup_app(app_: FastAPI):
    setup_cors(app_)
    setup_middlewares(app_)
    setup_exception_handlers(app_)
    setup_static_files(app_)

    # Set the rate limit handler
    app_.state.limiter = limiter

    # Include routers
    app_.include_router(api_router, prefix=settings.API_V1_STR)


def init_app() -> FastAPI:
    """Initializes and configures the FastAPI application."""
    # Create the application
    app_ = create_app()

    # Configure the application
    setup_app(app_)

    return app_


# Initialize the application
app = init_app()
