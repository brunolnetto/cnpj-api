from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from fastapi import BackgroundTasks
from time import strftime, localtime, perf_counter
from datetime import datetime
from backend.app.api.models.logs import RequestLogCreate
from backend.app.api.repositories.logs import RequestLogRepository
from backend.app.database.base import get_session
from backend.app.setup.config import settings


async def log_request(
    request_data: dict,
    response_data: dict,
    process_time: float,
    start_time: float,
):
    """
    This function runs in the background (via BackgroundTasks) and
    writes one RequestLog row to the audit database.
    """
    log_data = {
        "relo_method": request_data["method"],
        "relo_url": str(request_data["url"]),
        "relo_headers": request_data["headers"],
        "relo_status_code": response_data["status_code"],
        "relo_ip_address": request_data["client_host"],
        "relo_absolute_path": request_data["request_url"],
        "relo_device_info": request_data["user_agent"],
        "relo_request_duration_seconds": f"{process_time:.6f}",
        "relo_response_size": response_data["response_size"],
        "relo_inserted_at": strftime("%Y-%m-%d %H:%M:%S", localtime(start_time)),
    }

    # Open a short‐lived session and write to the audit table:
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as db_session:
        log = RequestLogCreate(**log_data)
        log_repository = RequestLogRepository(db_session)
        log_repository.create(log)


class AsyncRequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = perf_counter()

        # Let the request run through the rest of the stack (handlers, other middleware, etc.)
        original_response = await call_next(request)
        process_time = perf_counter() - start_time

        # If it's a StreamingResponse, we don't extract body‐chunks;
        # just attach BackgroundTasks to the existing response.
        if isinstance(original_response, StreamingResponse):
            wrapped_response = original_response
        else:
            # For non‐streaming responses, we need to reassemble the body so we can attach background tasks
            body_bytes = [chunk async for chunk in original_response.body_iterator]
            wrapped_response = Response(
                content=b"".join(body_bytes),
                status_code=original_response.status_code,
                headers=original_response.headers,
                media_type=original_response.media_type,
            )
            # Store the full body so that any downstream logic can still read it if needed:
            wrapped_response.body_bytes = b"".join(body_bytes)

        # Build the minimal, serializable request/response dicts:
        request_data = {
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "client_host": request.client.host,
            "user_agent": request.headers.get("user-agent", "Unknown"),
            "request_url": str(request.url),
        }

        response_data = {
            "status_code": original_response.status_code,
            "headers": dict(original_response.headers),
            "response_size": len(getattr(wrapped_response, "body_bytes", b"")),
        }

        # Create a BackgroundTasks object and hand off the log_request(...) call:
        background_tasks = BackgroundTasks()
        background_tasks.add_task(
            log_request,
            request_data,
            response_data,
            process_time,
            start_time,
        )

        # Attach it to the outgoing response. FastAPI will run it “in the background”
        # after the response is sent.
        wrapped_response.background = background_tasks

        return wrapped_response
