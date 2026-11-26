# Description: This file contains the setup routes for the FastAPI application.

import os
import toml
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from backend.app.api.rate_limiter import limiter

# Public on purpose: load balancers and uptime monitors call these without a token
router = APIRouter(tags=["Setup"])


class HealthCheckResponse(BaseModel):
    status: str


class InfoResponse(BaseModel):
    name: str
    version: str
    description: str


@router.get("/health", response_model=HealthCheckResponse)
@limiter.limit("5/minute")
async def health_check(request: Request) -> HealthCheckResponse:
    """
    Health check endpoint to verify if the service is running.
    """
    return HealthCheckResponse(status="OK")


@router.get("/info", response_model=InfoResponse)
@limiter.limit("5/minute")
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
        raise HTTPException(status_code=404, detail="Configuration file not found")
    except toml.TomlDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding configuration file")
