from datetime import datetime, timedelta, timezone

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from jose import jwt

from backend.app.api.dependencies.auth import (
    ClientStatusCache,
    JWTDependency,
    client_status_cache,
)
from backend.app.setup.config import settings
from backend.app.utils.security import create_token


ACTIVE_CLIENT = "cli_active"
INACTIVE_CLIENT = "cli_inactive"


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(
        client_status_cache, "lookup", lambda client_id: client_id == ACTIVE_CLIENT
    )
    client_status_cache.clear()

    app = FastAPI()

    @app.get("/protected", dependencies=[JWTDependency])
    def protected():
        return {"ok": True}

    return TestClient(app)


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_valid_token_is_accepted(client):
    response = client.get("/protected", headers=_auth(create_token({"sub": ACTIVE_CLIENT})))

    assert response.status_code == status.HTTP_200_OK


def test_expired_token_returns_expired_error(client):
    token = create_token({"sub": ACTIVE_CLIENT}, expires_delta=timedelta(seconds=-1))

    response = client.get("/protected", headers=_auth(token))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "expired" in response.json()["detail"].lower()


def test_invalid_token_is_rejected_without_internal_detail(client):
    response = client.get("/protected", headers=_auth("not-a-jwt"))

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Token is invalid"


def test_token_signed_with_other_key_is_rejected(client):
    token = jwt.encode({"sub": ACTIVE_CLIENT}, "another-secret-key-0123456789", "HS256")

    response = client.get("/protected", headers=_auth(token))

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_missing_token_is_rejected(client):
    response = client.get("/protected")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_token_lifetime_follows_settings():
    before = datetime.now(timezone.utc)
    token = create_token({"sub": ACTIVE_CLIENT})

    claims = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    lifetime = claims["exp"] - claims["iat"]

    assert lifetime == settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    assert abs(claims["iat"] - before.timestamp()) < 5


def test_token_without_subject_is_rejected(client):
    legacy_token = create_token({"message": "legacy signature"})

    response = client.get("/protected", headers=_auth(legacy_token))

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_token_of_inactive_client_is_rejected(client):
    token = create_token({"sub": INACTIVE_CLIENT})

    response = client.get("/protected", headers=_auth(token))

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_client_status_is_cached_until_ttl():
    calls = []

    def lookup(client_id):
        calls.append(client_id)
        return True

    cache = ClientStatusCache(lookup=lookup, ttl_seconds=60)

    assert cache.is_active("cli_a") is True
    assert cache.is_active("cli_a") is True
    assert calls == ["cli_a"]


def test_client_status_is_refreshed_after_ttl():
    statuses = iter([True, False])
    cache = ClientStatusCache(lookup=lambda _: next(statuses), ttl_seconds=0)

    assert cache.is_active("cli_a") is True
    assert cache.is_active("cli_a") is False
