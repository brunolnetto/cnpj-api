from backend.app.setup.config import settings
from backend.app.setup.logging import logger
from backend.app.api.app import app

# Log the application URL
logger.info(f"App running on {settings.server_host} for {app}")
