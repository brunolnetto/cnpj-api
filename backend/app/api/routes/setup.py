# Description: This file contains the setup routes for the FastAPI application.
from fastapi import APIRouter, Request
from pydantic import BaseModel
import toml
import time

from backend.app.setup.config import settings
from backend.app.api.dependencies.auth import JWTDependency
from backend.app.rate_limiter import limiter

router = APIRouter(tags=["Setup"], dependencies=[JWTDependency])


class ExampleResponse(BaseModel):
    message: str


@router.get("/benchmark")
def benchmark_serialization(data_size: int):
    data = {"message": "x" * data_size}
    
    start_time = time.time()
    ExampleResponse(**data)
    end_time = time.time()
    
    print(f"Serialization of size {data_size} took {end_time - start_time} seconds")


@router.get("/health")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def health_check(request: Request):
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "OK",
        "message": f"Visit {settings.API_V1_STR}/docs for more information.",
    }


@router.get("/info")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def info(request: Request):
    with open("pyproject.toml", "r", encoding="latin-1") as f:
        config = toml.load(f)

    return {
        "name": config["tool"]["poetry"]["name"],
        "version": config["tool"]["poetry"]["version"],
        "description": config["tool"]["poetry"]["description"],
    }
