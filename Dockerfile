# Use the official Python image as the base image
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install uv
RUN pip install uv

# Copy the rest of the application
COPY . .

# Install the dependencies
RUN uv sync

# Create directories for backend and static files
RUN mkdir -p /app/backend /app/static

# Command to run the FastAPI application
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
