from datetime import datetime, timedelta, timezone

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from jose import jwt

from backend.app.api.dependencies.auth import JWTDependency
from backend.app.setup.config import settings
from backend.app.utils.security import create_token


@pytest.fixture
def client():
    app = FastAPI()

    @app.get("/protected", dependencies=[JWTDependency])
    def protected():
        return {"ok": True}

    return TestClient(app)


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_valid_token_is_accepted(client):
    response = client.get("/protected", headers=_auth(create_token({"sub": "x"})))

    assert response.status_code == status.HTTP_200_OK


def test_expired_token_returns_expired_error(client):
    token = create_token({"sub": "x"}, expires_delta=timedelta(seconds=-1))

    response = client.get("/protected", headers=_auth(token))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "expired" in response.json()["detail"].lower()


def test_invalid_token_is_rejected_without_internal_detail(client):
    response = client.get("/protected", headers=_auth("not-a-jwt"))

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Token is invalid"


def test_token_signed_with_other_key_is_rejected(client):
    token = jwt.encode({"sub": "x"}, "another-secret-key-0123456789", "HS256")

    response = client.get("/protected", headers=_auth(token))

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_missing_token_is_rejected(client):
    response = client.get("/protected")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_token_lifetime_follows_settings():
    before = datetime.now(timezone.utc)
    token = create_token({"sub": "x"})

    claims = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    lifetime = claims["exp"] - claims["iat"]

    assert lifetime == settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    assert abs(claims["iat"] - before.timestamp()) < 5
