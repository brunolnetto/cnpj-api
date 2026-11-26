FROM python:3.12-slim-bookworm

# Pinned uv, installed from PyPI so the build only needs Docker Hub and PyPI
RUN pip install --no-cache-dir uv==0.13.5

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app" \
    # Install the locked dependencies into the image's Python
    UV_PROJECT_ENVIRONMENT=/usr/local \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Dependencies first, so this layer is cached until the lock changes
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-cache

# Create directories for backend and static files
RUN mkdir -p /app/backend /app/static

# Copy relevant files and folders into folder app
COPY backend /app/backend
COPY static /app/static
COPY .env .

# Command to run the FastAPI application
CMD [\
    "uvicorn", "backend.app.main:app", \
    "--host", "0.0.0.0", \
    "--port", "8000",\
    "--reload"\
]
