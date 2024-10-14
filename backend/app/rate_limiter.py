from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.app.setup.config import settings

# Initialize the Limiter with a global rate limit
limiter = Limiter(
    key_func=get_remote_address, default_limits=settings.DEFAULT_RATE_LIMITS
)
