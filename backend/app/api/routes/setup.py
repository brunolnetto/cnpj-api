# Description: This file contains the setup routes for the FastAPI application.
import time

import toml
from fastapi import APIRouter, Request
from pydantic import BaseModel

from backend.app.setup.config import settings
from backend.app.api.dependencies.auth import JWTDependency
from backend.app.rate_limiter import rate_limit

router = APIRouter(tags=["Setup"], dependencies=[JWTDependency])


class ExampleResponse(BaseModel):
    message: str


@rate_limit()
@router.get("/health")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def health_check(request: Request):
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "OK",
        "message": f"Visit {settings.API_V1_STR}/docs for more information.",
    }


@rate_limit()
@router.get("/info")
async def info(request: Request):
    with open("pyproject.toml", "r", encoding="latin-1") as f:
        config = toml.load(f)

    return {
        "name": config["tool"]["poetry"]["name"],
        "version": config["tool"]["poetry"]["version"],
        "description": config["tool"]["poetry"]["description"],
    }
