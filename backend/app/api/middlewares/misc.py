from time import perf_counter

from fastapi import Request, BackgroundTasks
from starlette.middleware.base import BaseHTTPMiddleware

from backend.app.setup.config import settings
from backend.app.database.models.logs import RequestTimingLog
from backend.app.database.base import get_session


class TimingMiddleware(BaseHTTPMiddleware):
    def save_request_timing(self, request: Request, process_time: float):
        # Save the request timing in the database
        with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
            request_timing = RequestTimingLog(
                rtlo_url_path=request.url.path,
                rtlo_method=request.method,
                rtlo_process_time=process_time,
            )
            session.add(request_timing)
            session.commit()

    async def dispatch(self, request: Request, call_next):
        # Record the start time
        start_time = perf_counter()

        # Process the request
        response = await call_next(request)

        # Calculate the time taken
        process_time = perf_counter() - start_time

        # Trigger a background task to save the execution time
        background_tasks = BackgroundTasks()
        background_tasks.add_task(self.save_request_timing, request, process_time)

        # Add background tasks to the response
        response.background = background_tasks

        return response
