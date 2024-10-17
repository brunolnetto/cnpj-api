# Description: This file contains the setup routes for the FastAPI application.

import toml
from fastapi import APIRouter, Request
from pydantic import BaseModel

from backend.app.api.dependencies.auth import JWTDependency
from backend.app.rate_limiter import rate_limit

router = APIRouter(tags=["Setup"], dependencies=[JWTDependency])


class ExampleResponse(BaseModel):
    message: str


@rate_limit()
@router.get("/health")
async def health_check(request: Request):
    return {
        "status": "OK",
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
