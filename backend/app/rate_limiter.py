from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.app.setup.config import settings

# Initialize the Limiter with a global rate limit
limiter = Limiter(
    key_func=get_remote_address, 
    default_limits=settings.DEFAULT_RATE_LIMITS
)

# Disable rate limiting in development
DISABLE_RATE_LIMITING = settings.ENVIRONMENT == "development"

# Create a custom decorator with optional rate limit configuration
def rate_limit(rate_limit_config: str = settings.DEFAULT_RATE_LIMIT):
    def decorator(func):
        if DISABLE_RATE_LIMITING:
            return func

        return limiter.limit(rate_limit_config)(func)

    return decorator
