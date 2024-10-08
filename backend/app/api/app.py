# Description: This file initializes the FastAPI application and sets up
# configurations.
from contextlib import asynccontextmanager
from asyncio import create_task
from time import perf_counter

from fastapi import FastAPI, status, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from backend.app.setup.config import settings
from backend.app.setup.logging import logger
from backend.app.api.routes.router_bundler import api_router
from backend.app.api.exceptions import (
    not_found_handler,
    general_exception_handler,
    custom_rate_limit_handler,
)
from backend.app.api.middlewares.logs import AsyncRequestLoggingMiddleware
from backend.app.api.utils.misc import print_execution_time
from backend.app.api.middlewares.misc import TimingMiddleware
from backend.app.api.dependencies.logs import log_app_start
from backend.app.api.dependencies.cnpj import initialize_CNPJRepository_on_startup
from backend.app.database.base import init_database, multi_database
from backend.app.api.utils.ml import init_nltk
from backend.app.scheduler.bundler import task_orchestrator, add_tasks
from backend.app.rate_limiter import rate_limit
from backend.app.setup.logging import setup_logger


@asynccontextmanager
async def lifespan(app_: FastAPI):
    """
    The `lifespan` async context manager in Python initializes and cleans up various
    tasks for a FastAPI application.

    :param app: The `app` parameter in the `lifespan` async context manager function is of type
    `FastAPI`. It is likely being used to pass in the FastAPI application instance to perform
    initialization and cleanup tasks related to the application's lifespan
    :type app: FastAPI
    """
    
    # Data related entities
    print_execution_time(init_database)()
    
    # Logging
    await print_execution_time(setup_logger)()
    
    # Initialize CNPJ repository
    print_execution_time(initialize_CNPJRepository_on_startup)()

    # Log app startup
    print_execution_time(log_app_start)()

    # Start task orchestrator
    await print_execution_time(task_orchestrator.start)()

    # Add tasks to orchestrator
    await print_execution_time(add_tasks)()

    # Initialize NLTK
    print_execution_time(init_nltk)()

    yield

    # Cleanup tasks
    await print_execution_time(task_orchestrator.shutdown)()

    # Disconnect from databases
    print_execution_time(multi_database.disconnect)()


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
    # Middlewares
    ##########################################################################
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

    # Add request logging middleware
    app_.add_middleware(AsyncRequestLoggingMiddleware)

    # Add gzip middleware
    app_.add_middleware(GZipMiddleware, minimum_size=1000)

    # Add timing middleware
    app_.add_middleware(TimingMiddleware)

    ##########################################################################
    # Static files
    ##########################################################################
    obj = StaticFiles(directory="static")
    app_.mount("/static", obj, name="static")

    ##########################################################################
    # Favicon file
    ##########################################################################
    @rate_limit()
    @app_.get("/favicon.ico", include_in_schema=False)
    async def get_favicon(request: Request):
        return FileResponse("static/favicon.ico")

    ##########################################################################
    # Exceptions
    ##########################################################################
    # Add exception handlers
    app_.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)
    app_.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_handler)
    app_.add_exception_handler(Exception, general_exception_handler)


def init_app():
    # Get the number of applications from the environment variable
    app_ = create_app()

    # Setup the application
    setup_app(app_)

    return app_


# Initialize the application
app = init_app()
