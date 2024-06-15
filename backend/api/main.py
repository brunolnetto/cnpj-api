from uvicorn import run

from backend.api.app import app
from backend.setup.config import settings
from backend.setup.logging import logger

# Run the application
if __name__ == "__main__":
    # Run the FastAPI application
    run(app, host=settings.APP_HOST, port=settings.APP_PORT)

    # Log the application URL
    logger.info(f"🚀 App running on {settings.server_host}")
