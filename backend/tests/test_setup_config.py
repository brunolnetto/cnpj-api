import pytest
from pydantic import ValidationError

from backend.app.setup.config import Settings

BASE_SETTINGS = {
    "POSTGRES_HOST": "localhost",
    "POSTGRES_USER": "user",
    "POSTGRES_PASSWORD": "a-strong-password",
    "DEFAULT_RATE_LIMIT": "10/minute",
    "DEFAULT_BURST_RATE_LIMIT": "500/hour",
}

KNOWN_SECRET = "dev-only-insecure-secret-change-me"


def test_production_rejects_known_jwt_secret():
    with pytest.raises(ValidationError, match="publicly known"):
        Settings(**BASE_SETTINGS, ENVIRONMENT="production", JWT_SECRET_KEY=KNOWN_SECRET)


def test_development_warns_on_known_jwt_secret():
    with pytest.warns(UserWarning, match="publicly known"):
        Settings(
            **BASE_SETTINGS, ENVIRONMENT="development", JWT_SECRET_KEY=KNOWN_SECRET
        )


def test_production_accepts_unknown_jwt_secret():
    settings = Settings(
        **BASE_SETTINGS, ENVIRONMENT="production", JWT_SECRET_KEY="f" * 64
    )

    assert settings.JWT_SECRET_KEY == "f" * 64
