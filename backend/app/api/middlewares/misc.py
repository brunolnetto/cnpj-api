import time
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Record the start time
        start_time = time.perf_counter()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate the time taken
        process_time = time.perf_counter() - start_time
        
        # Log the time taken
        print(f"Request: {request.url.path} took {process_time:.4f} seconds")
        
        return response