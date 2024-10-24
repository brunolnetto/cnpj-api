# Description: This file initializes the FastAPI application and sets up
# configurations.
from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, status, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded


from backend.app.setup.config import settings
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
    t0=perf_counter()

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

    print(f"Start up took {perf_counter()-t0} seconds")

    yield

    t0=perf_counter()

    # Cleanup tasks
    await print_execution_time(task_orchestrator.shutdown)()

    # Disconnect from databases
    print_execution_time(multi_database.disconnect)()

    print(f"Shutdown took {perf_counter()-t0} seconds")    

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


def setup_cors(app: FastAPI) -> None:
    """Sets up CORS middleware for the application."""
    if settings.BACKEND_CORS_ORIGINS:
        urls = [str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=urls,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def setup_middlewares(app: FastAPI) -> None:
    """Adds middleware to the FastAPI application."""
    app.add_middleware(AsyncRequestLoggingMiddleware)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(TimingMiddleware)


def setup_static_files(app: FastAPI) -> None:
    """Sets up static file serving for the FastAPI application."""
    app.mount("/static", StaticFiles(directory="static"), name="static")


def setup_favicon(app: FastAPI) -> None:
    """Sets up the favicon endpoint for the FastAPI application."""

    @rate_limit()
    @app.get("/favicon.ico", include_in_schema=False)
    async def get_favicon(request: Request):
        return FileResponse("static/favicon.ico")


def setup_exception_handlers(app: FastAPI) -> None:
    """Sets up exception handlers for the FastAPI application."""
    app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)
    app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_handler)
    app.add_exception_handler(Exception, general_exception_handler)

def setup_app(app_: FastAPI):
    setup_cors(app_)
    setup_middlewares(app_)
    setup_static_files(app_)
    setup_favicon(app_)
    setup_exception_handlers(app_)
    
    app_.include_router(api_router, prefix=settings.API_V1_STR)

def init_app() -> FastAPI:
    """Initializes and configures the FastAPI application."""
    app = create_app()
    
    setup_app(app)

    return app


# Initialize the application
app = init_app()
