"""
import pytest

from fastapi.testclient import TestClient
from backend.api.routes.setup import router  

from backend.setup.config import settings

pytestmark = pytest.mark.asyncio


async def test_ping():
    with TestClient(app=router) as client:
        response = await client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"message": "pong"}


async def test_health_check():
    with TestClient(app=router) as client:
        # Simulate settings with example values
        settings.PROJECT_NAME = "My Awesome Project"
        settings.VERSION = "1.0.0"
        settings.API_V1_STR = "/api/v1"

        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "status": "OK",
            "message": f"Visit {settings.API_V1_STR}/docs for more information.",
        }


async def test_info():
    # Mock the toml library to avoid reading the actual file
    with pytest.MonkeyPatch.context() as mp:
        mp.patch("toml.load", return_value={"tool": {"poetry": {"name": "my-package", "version": "0.1.0", "description": "A cool package"}}})

        with TestClient(app=router) as client:
            response = await client.get("/info")
            assert response.status_code == 200
            assert response.json() == {
                "name": "my-package",
                "version": "0.1.0",
                "description": "A cool package",
            }

"""
