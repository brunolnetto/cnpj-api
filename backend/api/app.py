# Description: This file initializes the FastAPI application and sets up configurations.

from fastapi import FastAPI, status, Request, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

import sentry_sdk

from backend.setup.config import settings
from backend.api.routes.router_bundler import api_router


def custom_generate_unique_id(route: APIRoute) -> str:
    tag = "" if not route.tags else route.tags[0]
    name = route.name
    route_label = f"{tag}-{name}" if tag else name

    return route_label


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
    )

    @app_.get("/favicon.ico")
    async def get_favicon():
        return FileResponse("static/favicon.ico")

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
        """Redirects to docs or redoc on 404 Not Found."""
        # Choose between docs or redoc based on your preference
        redirect_url = f"{settings.API_V1_STR}/docs"  # Or "/redoc"
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)

    # Sentry configuration
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            traces_sample_rate=1.0,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=1.0,
        )

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app_.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
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
