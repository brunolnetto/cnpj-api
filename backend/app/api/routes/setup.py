# Description: This file contains the setup routes for the FastAPI application.
from fastapi import APIRouter, Request
import toml

from backend.app.setup.config import settings
from backend.app.utils.security import create_token

router = APIRouter(
    tags=["Setup"]
)

@router.get('/token')
async def get_token():
    return {
        "access_token": create_token({}),
    }

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
