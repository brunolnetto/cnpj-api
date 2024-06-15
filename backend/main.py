from uvicorn import run

from backend.api.app import app
from backend.setup.config import settings
from backend.setup.logging import logger

# Log the application URL
logger.info(f"App running on {settings.server_host}")
