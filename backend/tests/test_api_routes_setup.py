import pytest

from fastapi.testclient import TestClient
from backend.app.api.routes.setup import router  
from backend.app.setup.config import settings


@pytest.mark.asyncio
async def test_health_check():
    with TestClient(app=router) as client:
        # Simulate settings with example values
        settings.PROJECT_NAME = "My Awesome Project"
        settings.VERSION = "1.0.0"
        settings.API_V1_STR = "/api/v1"

        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "status": "OK",
            "message": f"Visit {settings.API_V1_STR}/docs for more information.",
        }

@pytest.mark.asyncio
async def test_info():
    # Mock the toml library to avoid reading the actual file
    with pytest.MonkeyPatch.context() as mp:
        info_dict={
            "name": "my-package", 
            "version": "0.1.0", 
            "description": "A cool package"
        }
        mp.setattr("toml.load", lambda _: { "tool": { "poetry": info_dict }})

        with TestClient(app=router) as client:
            response = client.get("/info")
            assert response.status_code == 200
            assert response.json() == info_dict
