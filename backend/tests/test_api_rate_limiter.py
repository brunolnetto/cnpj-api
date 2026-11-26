from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from jose import jwt
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from backend.app.api.rate_limiter import rate_limit_key
from backend.app.setup.config import settings
from backend.app.utils.security import create_token

TRAEFIK_IP = "10.0.1.5"
CLIENT_IP = "203.0.113.7"


def _key_for(headers=None, trusted_hosts=None) -> str:
    app = FastAPI()

    @app.get("/key")
    def key(request: Request):
        return {"key": rate_limit_key(request)}

    asgi_app = (
        ProxyHeadersMiddleware(app, trusted_hosts=trusted_hosts)
        if trusted_hosts
        else app
    )
    client = TestClient(asgi_app, client=(TRAEFIK_IP, 50000))

    return client.get("/key", headers=headers or {}).json()["key"]


def test_valid_token_is_limited_per_client():
    token = create_token({"sub": "cli_abc"})

    assert _key_for({"Authorization": f"Bearer {token}"}) == "client:cli_abc"


def test_forged_token_falls_back_to_ip():
    forged = jwt.encode({"sub": "cli_victim"}, "not-the-real-secret-0123", "HS256")

    key = _key_for({"Authorization": f"Bearer {forged}"})

    assert key == f"ip:{TRAEFIK_IP}"


def test_expired_token_falls_back_to_ip():
    from datetime import timedelta

    expired = create_token({"sub": "cli_abc"}, expires_delta=timedelta(seconds=-1))

    assert _key_for({"Authorization": f"Bearer {expired}"}).startswith("ip:")


def test_without_trusted_proxy_every_client_shares_the_proxy_ip():
    key = _key_for({"X-Forwarded-For": CLIENT_IP})

    assert key == f"ip:{TRAEFIK_IP}"


def test_trusted_proxy_exposes_the_real_client_ip():
    key = _key_for({"X-Forwarded-For": CLIENT_IP}, trusted_hosts="10.0.0.0/8")

    assert key == f"ip:{CLIENT_IP}"


def test_untrusted_proxy_cannot_spoof_client_ip():
    key = _key_for({"X-Forwarded-For": CLIENT_IP}, trusted_hosts="192.168.0.0/16")

    assert key == f"ip:{TRAEFIK_IP}"


def test_default_storage_is_memory():
    assert settings.RATE_LIMIT_STORAGE_URI == "memory://"
