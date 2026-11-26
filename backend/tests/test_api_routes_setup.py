import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.rate_limiter import limiter
from backend.app.api.routes.setup import router


@pytest.fixture
def client():
    app = FastAPI()
    app.state.limiter = limiter
    app.include_router(router)

    limiter.reset()
    yield TestClient(app)
    limiter.reset()


def test_health_check_does_not_require_token(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_info_does_not_require_token(client, monkeypatch):
    info_dict = {
        "name": "my-package",
        "version": "0.1.0",
        "description": "A cool package",
    }
    monkeypatch.setattr("toml.load", lambda _: {"tool": {"poetry": info_dict}})

    response = client.get("/info")

    assert response.status_code == 200
    assert response.json() == info_dict
