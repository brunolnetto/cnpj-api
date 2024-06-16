
from backend.api.app import app
from backend.setup.config import settings
from backend.setup.logging import logger

# Log the application URL
logger.info(f"App running on {settings.server_host}")

if __name__ == "__main__":
    app.run(host=settings.server_host, port=settings.server_port)
