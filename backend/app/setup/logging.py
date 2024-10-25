import logging
import sys

from dotenv import load_dotenv
from pythonjsonlogger import jsonlogger

from backend.app.setup.config import settings
from backend.app.api.dependencies.logs import get_debug_logs_handler

# Advanced logger
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Define logging format
fields = [
    "name",
    "process",
    "processName",
    "threadName",
    "thread",
    "taskName",
    "asctime",
    "created",
    "relativeCreated",
    "msecs",
    "pathname",
    "module",
    "filename",
    "funcName",
    "levelno",
    "levelname",
    "message",
]
logging_format = " ".join(map(lambda field_name: f"%({field_name})s", fields))
fmt = jsonlogger.JsonFormatter(logging_format)


async def setup_logger():
    try:
        # Set up database logging handler
        db_handler = get_debug_logs_handler()
        db_handler.setLevel(logging.INFO)
        db_handler.setFormatter(fmt)
        logger.addHandler(db_handler)
        logger.info("Database logging started.")

    except Exception as e:
        # Handle exceptions with setting up database logging
        print(f"Error setting up database logging: {e}", file=sys.stderr)
        # You might want to raise an exception or log it to a file

    if settings.ENVIRONMENT == "development":
        # Set up stdout and stderr handlers for development
        stdout_stream_handler = logging.StreamHandler(sys.stdout)
        stderr_stream_handler = logging.StreamHandler(sys.stderr)
        stdout_stream_handler.setFormatter(fmt)
        stderr_stream_handler.setFormatter(fmt)

        # Apply basic configuration with these handlers
        logging.basicConfig(
            level=logging.INFO,
            handlers=[stdout_stream_handler])
        logging.basicConfig(
            level=logging.WARN,
            handlers=[stderr_stream_handler])


logger.info("Logging started.")
