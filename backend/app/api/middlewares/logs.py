from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from time import time, strftime, localtime

from backend.app.api.models.logs import RequestLogCreate
from backend.app.api.repositories.logs import RequestLogRepository
from backend.app.database.base import get_session
from backend.app.scheduler.bundler import task_orchestrator
from backend.app.setup.config import settings


async def capture_request_body(request: Request):
    if not hasattr(request.state, "body"):
        # Read the body only once and store it in request.state
        request.state.body = await request.body()
    return request.state.body.decode() if request.state.body else ""


background_scheduler = task_orchestrator.schedulers["background"]


class AsyncRequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time()

        # Call the next middleware or endpoint
        response: Response = await call_next(request)

        process_time = time() - start_time

        # Capture the response body for streaming responses
        response_body = b""

        async def log_body_iterator(body_iterator):
            nonlocal response_body
            async for chunk in body_iterator:
                response_body += chunk
                yield chunk  # Yield the chunk for the StreamingResponse

        # If the response is a StreamingResponse, capture the body
        if hasattr(response, "body_iterator"):
            response.body_iterator = log_body_iterator(response.body_iterator)

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

        # Schedule the log entry as a background task
        background_scheduler.add_job(
            self.log_request,
            args=[log_data],
            id=f"log-{strftime('%Y%m%d%H%M%S', localtime(start_time))}",
        )

        # Return the original response
        return response

    @staticmethod
    def log_request(log_data):
        print(log_data)
        # This function runs in the background to log the request details
        with get_session(settings.POSTGRES_DBNAME_AUDIT) as db_session:
            log = RequestLogCreate(**log_data)
            log_repository = RequestLogRepository(db_session)
            log_repository.create(log)
