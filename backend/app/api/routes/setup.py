# Description: This file contains the setup routes for the FastAPI application.
from fastapi import APIRouter, Request
import toml

from backend.app.setup.config import settings

router = APIRouter(
    tags=["Setup"]
)


@router.get("/request-info")
async def get_request_info(request: Request):
    """
    Get information about the incoming request.

    Parameters:
    - request: The incoming request object.

    Returns:
    - A dictionary with information about the request.
    """
    headers = request.headers

    # Access other request attributes as needed (e.g., headers, body)
    return {
        "client": request.client,
        "base_url": request.base_url,
        "url": request.url,
        "method": request.method,
        "query_params": request.query_params,
        "path_params": request.path_params,
        "headers": headers,
        "cookies": request.cookies,
        "body": await request.body(),
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
