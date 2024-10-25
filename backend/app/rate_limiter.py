from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.app.setup.config import settings
from backend.app.setup.logging import logger

# Initialize the Limiter with a global rate limit
limiter = Limiter(
    key_func=get_remote_address, default_limits=settings.DEFAULT_RATE_LIMITS
)

# Disable rate limiting in development
DISABLE_RATE_LIMITING = settings.ENVIRONMENT == "development"


def rate_limit(
        rate_limit_config: str = settings.DEFAULT_RATE_LIMIT) -> callable:
    """
    A decorator to apply rate limiting to a function.

    Args:
        rate_limit_config (str): The rate limit configuration string.

    Returns:
        callable: The decorated function with rate limiting applied, or the original function if disabled.
    """

    def decorator(func: callable) -> callable:
        logger.info(f"Rate limiting enabled: {not DISABLE_RATE_LIMITING}")

        if DISABLE_RATE_LIMITING:
            return func

        logger.info(
            f"Applying rate limit: {rate_limit_config} to {func.__name__}")

        return limiter.limit(rate_limit_config)(func)

    return decorator
