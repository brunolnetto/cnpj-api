from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
from time import strftime, localtime
import asyncio

from backend.app.api.models.logs import RequestLogCreate
from backend.app.api.repositories.logs import RequestLogRepository
from backend.app.database.base import get_session
from backend.app.scheduler.bundler import task_orchestrator
from backend.app.setup.config import settings


async def capture_request_body(request: Request):
    if not hasattr(request.state, "body"):
        # Only read body if required (skip for GET, etc.)
        if request.method not in ("POST", "PUT", "PATCH"):
            request.state.body = b""
        else:
            request.state.body = await request.body()
    
    return request.state.body.decode() if request.state.body else ""


background_scheduler = task_orchestrator.schedulers["background"]


class AsyncRequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        # Proceed to next middleware/endpoint
        response: Response = await call_next(request)

        response_t = time.perf_counter()

        process_time = response_t - start_time

        # Log response body size (only for non-streaming)
        response_body = await response.body() if hasattr(response, "body") else b""
        response_size = len(response_body)

        # Prepare log data
        log_data = {
            "relo_method": request.method,
            "relo_url": str(request.url),
            "relo_headers": dict(request.headers),
            "relo_status_code": response.status_code,
            "relo_ip_address": request.client.host,
            "relo_device_info": request.headers.get("user-agent", "Unknown"),
            "relo_absolute_path": str(request.url),
            "relo_request_duration_seconds": f"{process_time:.6f}",
            "relo_response_size": response_size,
            "relo_inserted_at": strftime("%Y-%m-%d %H:%M:%S", localtime(start_time)),
        }

        # Schedule logging asynchronously after returning response
        asyncio.create_task(self.log_request(log_data))

        # Return the original response
        return response

    @staticmethod
    async def log_request(log_data):
        # Log asynchronously in the background
        with get_session(settings.POSTGRES_DBNAME_AUDIT) as db_session:
            log = RequestLogCreate(**log_data)
            log_repository = RequestLogRepository(db_session)
            log_repository.create(log)
