from time import perf_counter
from typing import Any, Callable, Dict

from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from backend.app.api.models.logs import RequestLogCreate
from backend.app.api.repositories.logs import RequestLogRepository
from backend.app.database.base import get_session
from backend.app.setup.config import settings
from backend.app.setup.logging import logger

REDACTED = "[REDACTED]"

# Headers that carry credentials and must never be persisted
SENSITIVE_HEADERS = frozenset(
    {
        "authorization",
        "proxy-authorization",
        "cookie",
        "set-cookie",
        "x-api-key",
    }
)


def redact_headers(headers) -> dict:
    """Return a copy of the headers with credential-bearing values masked."""
    return {
        key: REDACTED if key.lower() in SENSITIVE_HEADERS else value
        for key, value in headers.items()
    }


def persist_request_log(log_data: Dict[str, Any]) -> None:
    """Write one RequestLog row to the audit database."""
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as db_session:
        RequestLogRepository(db_session).create(RequestLogCreate(**log_data))


class RequestAuditMiddleware:
    """
    Records each HTTP request (method, URL, redacted headers, status, duration
    and response size) in the audit database with a single write.

    Pure ASGI: the response streams through untouched; the body size is counted
    from the chunks as they are sent instead of buffering the whole body.
    """

    def __init__(
        self,
        app: ASGIApp,
        persist: Callable[[Dict[str, Any]], None] = persist_request_log,
    ):
        self.app = app
        self.persist = persist

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = perf_counter()
        # Stays 500 if the app fails before starting a response
        status_code = 500
        response_size = 0

        async def send_and_measure(message: Message) -> None:
            nonlocal status_code, response_size

            if message["type"] == "http.response.start":
                status_code = message["status"]
            elif message["type"] == "http.response.body":
                response_size += len(message.get("body", b""))

            await send(message)

        try:
            await self.app(scope, receive, send_and_measure)
        finally:
            # The response has been sent by now: the write does not delay it
            request = Request(scope)
            client_host = request.client.host if request.client else None
            url = str(request.url)

            log_data = {
                "relo_method": request.method,
                "relo_url": url,
                "relo_headers": redact_headers(request.headers),
                "relo_status_code": status_code,
                "relo_ip_address": client_host,
                "relo_absolute_path": url,
                "relo_device_info": request.headers.get("user-agent", "Unknown"),
                "relo_request_duration_seconds": perf_counter() - start_time,
                "relo_response_size": response_size,
            }

            try:
                await run_in_threadpool(self.persist, log_data)
            except Exception as e:  # Auditing must never break a request
                logger.error(f"Failed to persist request log for {url}: {e}")
