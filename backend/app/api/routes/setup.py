# Description: This file contains the setup routes for the FastAPI application.

import toml
import os
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from backend.app.api.dependencies.auth import JWTDependency
from backend.app.api.rate_limiter import limiter
from backend.app.setup.config import settings

router = APIRouter(tags=["Setup"], dependencies=[JWTDependency])


class HealthCheckResponse(BaseModel):
    status: str


class InfoResponse(BaseModel):
    name: str
    version: str
    description: str


@limiter.limit("5/minute")
@router.get("/health", response_model=HealthCheckResponse)
async def health_check(request: Request) -> HealthCheckResponse:
    """
    Health check endpoint to verify if the service is running.
    """
    return HealthCheckResponse(status="OK")


@limiter.limit("5/minute")
@router.get("/info", response_model=InfoResponse)
async def info(request: Request) -> InfoResponse:
    """
    Endpoint to retrieve application information from the pyproject.toml file.
    """
    toml_path = os.getenv(
        "PYPROJECT_TOML_PATH", "pyproject.toml"
    )  # Use env variable for path
    try:
        with open(toml_path, "r", encoding="utf-8") as f:
            config = toml.load(f)

        return InfoResponse(
            name=config["tool"]["poetry"]["name"],
            version=config["tool"]["poetry"]["version"],
            description=config["tool"]["poetry"]["description"],
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Configuration file not found")
    except toml.TomlDecodeError:
        raise HTTPException(status_code=500,
                            detail="Error decoding configuration file")
