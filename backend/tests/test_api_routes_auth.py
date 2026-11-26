import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from jose import jwt

from backend.app.api.rate_limiter import limiter
from backend.app.api.routes import auth
from backend.app.setup.config import settings

CLIENT_ID = "cli_test"
CLIENT_SECRET = "correct-secret"


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(
        auth,
        "_authenticate",
        lambda client_id, client_secret: (client_id, client_secret)
        == (CLIENT_ID, CLIENT_SECRET),
    )

    app = FastAPI()
    app.state.limiter = limiter
    app.include_router(auth.router)

    limiter.reset()
    yield TestClient(app)
    limiter.reset()


def test_token_is_issued_for_valid_credentials_without_a_token(client):
    response = client.post(
        "/token", json={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    claims = jwt.decode(
        body["access_token"],
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
    assert claims["sub"] == CLIENT_ID


def test_invalid_credentials_are_rejected(client):
    response = client.post(
        "/token", json={"client_id": CLIENT_ID, "client_secret": "wrong"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid client credentials."


def test_missing_credentials_are_rejected(client):
    response = client.post("/token", json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
