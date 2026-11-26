from jose import JWTError, jwt
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from backend.app.setup.config import settings


def rate_limit_key(request: Request) -> str:
    """
    Rate limit per API client when the request carries a valid token, and per
    client IP otherwise.

    The token signature is verified so a forged subject cannot be used to get a
    fresh quota. The client IP is the real one only when uvicorn trusts the
    reverse proxy (FORWARDED_ALLOW_IPS); otherwise it is the proxy's IP.
    """
    scheme, _, token = request.headers.get("authorization", "").partition(" ")

    if scheme.lower() == "bearer" and token:
        try:
            payload = jwt.decode(
                token.strip(),
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except JWTError:
            payload = {}

        client_id = payload.get("sub")
        if client_id:
            return f"client:{client_id}"

    return f"ip:{get_remote_address(request)}"


# Initialize the Limiter with a global rate limit
limiter = Limiter(
    key_func=rate_limit_key,
    default_limits=settings.DEFAULT_RATE_LIMITS,
    storage_uri=settings.RATE_LIMIT_STORAGE_URI,
)

# Disable rate limiting in development
DISABLE_RATE_LIMITING = settings.ENVIRONMENT == "development"


def rate_limit() -> callable:
    """
    A decorator to apply rate limiting to a function.

    Returns:
        callable: The decorated function with rate limiting applied, or the original 
        function if disabled.
    """

    def decorator(func: callable) -> callable:
        if DISABLE_RATE_LIMITING:
            return func

        decorated_func = limiter.limit(settings.DEFAULT_RATE_LIMIT)(func)
        return decorated_func

    return decorator
