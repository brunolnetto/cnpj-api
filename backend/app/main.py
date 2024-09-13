from backend.app.setup.config import settings
from backend.app.setup.logging import logger

# Log the application URL
logger.info(f"App running on {settings.server_host}")
