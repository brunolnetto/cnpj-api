from backend.app.api.app import app
from backend.app.setup.config import settings
from backend.app.setup.logging import logger

# Log the application URL
logger.info(f"App running on {settings.server_host}")

if __name__ == "__main__":
    app.run(host=settings.server_host, port=settings.server_port)
