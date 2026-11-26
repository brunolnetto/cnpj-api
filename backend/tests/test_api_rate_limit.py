from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from backend.app.api.app import app
from backend.app.api.dependencies.auth import jwt_bearer
from backend.app.api.rate_limiter import limiter
from backend.app.api.routes import setup


def _route_name(func) -> str:
    return f"{func.__module__}.{func.__name__}"


def test_rate_limited_routes_register_the_limiter_wrapper():
    """
    SlowAPIMiddleware skips routes that have their own limit, trusting the
    decorator to enforce it. If the route decorator sits above the limiter
    decorator, FastAPI registers the unwrapped function and no limit applies.
    """
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue

        if _route_name(route.endpoint) in limiter._route_limits:
            assert hasattr(route.endpoint, "__wrapped__"), (
                f"{route.path} declares a rate limit but its registered "
                "endpoint is not the limiter wrapper"
            )


def test_route_limit_returns_429_when_exceeded():
    test_app = FastAPI()
    test_app.state.limiter = limiter
    test_app.add_middleware(SlowAPIMiddleware)
    test_app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    test_app.include_router(setup.router)
    test_app.dependency_overrides[jwt_bearer] = lambda: {}

    limiter.reset()
    client = TestClient(test_app)

    # /health is limited to 5/minute
    statuses = [client.get("/health").status_code for _ in range(6)]

    assert statuses[:5] == [200] * 5
    assert statuses[5] == 429

    limiter.reset()
