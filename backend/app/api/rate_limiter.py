from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.app.setup.config import settings

# Initialize the Limiter with a global rate limit
limiter = Limiter(
    key_func=get_remote_address, default_limits=settings.DEFAULT_RATE_LIMITS
)

def rate_limit() -> callable:
    """
    A decorator to apply rate limiting to a function.

    Args:
        rate_limit_config (str): The rate limit configuration string.

    Returns:
        callable: The decorated function with rate limiting applied, or the original function if disabled.
    """

    def decorator(func):        
        return limiter.limit(settings.DEFAULT_RATE_LIMIT)(func)

    return decorator

def rate_limit(rate_limit_config: str = '3/minute',):
    def decorator(func):        
        return limiter.limit(rate_limit_config)(func)

    return decorator
