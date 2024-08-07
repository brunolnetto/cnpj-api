# Description: This file contains the setup routes for the FastAPI application.
from fastapi import APIRouter
import toml

from backend.app.setup.config import settings
from backend.app.api.dependencies.auth import JWTDependency


router = APIRouter(tags=["Setup"], dependencies=[JWTDependency])


@router.get("/health")
async def health_check():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "OK",
        "message": f"Visit {settings.API_V1_STR}/docs for more information.",
    }


@router.get("/info")
async def info():
    with open("pyproject.toml", "r", encoding="latin-1") as f:
        config = toml.load(f)

    return {
        "name": config["tool"]["poetry"]["name"],
        "version": config["tool"]["poetry"]["version"],
        "description": config["tool"]["poetry"]["description"],
    }
