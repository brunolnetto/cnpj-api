from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from time import strftime, localtime, perf_counter
from uuid import uuid4
from datetime import datetime, timedelta

from backend.app.api.models.logs import RequestLogCreate
from backend.app.api.repositories.logs import RequestLogRepository
from backend.app.database.base import get_session
from backend.app.api.models.tasks import TaskConfig
from backend.app.scheduler.bundler import task_orchestrator
from backend.app.scheduler.base import ScheduledTask
from backend.app.setup.config import settings

background_scheduler = task_orchestrator.schedulers["background"]


async def capture_request_body(request: Request):
    if not hasattr(request.state, "body"):
        # Only read body if required (skip for GET, etc.)
        if request.method not in ("POST", "PUT", "PATCH"):
            request.state.body = b""
        else:
            request.state.body = await request.body()

    return request.state.body.decode() if request.state.body else ""


async def log_request(
    request_data, response_data, process_time: float, start_time: float
):
    # Define log_request as a standalone function
    log_data = {
        "relo_method": request_data["method"],
        "relo_url": str(
            request_data["url"]),
        "relo_headers": request_data["headers"],
        "relo_status_code": response_data["status_code"],
        "relo_ip_address": request_data["client_host"],
        "relo_absolute_path": request_data["request_url"],
        "relo_device_info": request_data["user_agent"],
        "relo_request_duration_seconds": f"{process_time:.6f}",
        "relo_response_size": response_data["response_size"],
        "relo_inserted_at": strftime(
            "%Y-%m-%d %H:%M:%S",
            localtime(start_time)),
    }

    with get_session(settings.POSTGRES_DBNAME_AUDIT) as db_session:
        log = RequestLogCreate(**log_data)
        log_repository = RequestLogRepository(db_session)
        log_repository.create(log)


class AsyncRequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = perf_counter()

        # Proceed to the next middleware or the actual request handler
        original_response = await call_next(request)

        response_t = perf_counter()
        process_time = response_t - start_time

        # For StreamingResponse, do not capture body, avoid recursive calls
        if isinstance(original_response, StreamingResponse):
            wrapped_response = original_response
        else:
            # Capture the response body (non-streaming responses)
            body_bytes = [chunk async for chunk in original_response.body_iterator]
            wrapped_response = Response(
                b"".join(body_bytes),
                status_code=original_response.status_code,
                headers=original_response.headers,
            )
            wrapped_response.body_bytes = b"".join(
                body_bytes)  # Store full body

        # Extract serializable data from request and response
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
            "response_size": len(
                wrapped_response.body_bytes
                if hasattr(wrapped_response, "body_bytes")
                else b""
            ),
        }

        # Create the task configuration with a future delay
        task_id = uuid4()
        # Create the task configuration with a future delay
        task_config = TaskConfig(
            task_id=task_id,
            schedule_type="background",
            task_name=f"log_request_{task_id}",
            task_type="date",  # Use 'date' type for future execution
            task_callable=log_request,
            # The log_request function should now only take serializable
            # arguments
            task_args=[request_data, response_data, process_time, start_time],
            schedule_params={
                "run_time": datetime.now() +
                timedelta(
                    seconds=5)},
            # Delay execution by 5 seconds
            task_details={},  # No additional details required for this task
        )

        # Schedule the logging task using TaskOrchestrator and ScheduledTask
        scheduled_task = ScheduledTask(task_config)

        scheduled_task.schedule(background_scheduler)

        # Return the response without waiting for logging
        return wrapped_response
