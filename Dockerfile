# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app"

# Install uv
RUN pip install uv

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN uv pip install --no-cache-dir -r requirements.txt --system && \
    pip install --upgrade pip

# Create directories for backend and static files
RUN mkdir -p /app/backend /app/static

# Copy relevant files and folders into folder app
COPY backend /app/backend
COPY static /app/static
COPY pyproject.toml .
COPY .env .

# Command to run the FastAPI application
CMD [\
    "uvicorn", "backend.app.main:app", \
    "--host", "0.0.0.0", \
    "--port", "8000"\
]

