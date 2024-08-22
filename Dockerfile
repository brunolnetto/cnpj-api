# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for backend and static files
RUN mkdir -p /app/backend /app/static

# Copy the backend and static folders into their respective directories
COPY ./backend /app/backend
COPY ./static /app/static

# Copy the .env and pyproject.toml file into the working directory
COPY ./.env .

COPY ./pyproject.toml .

# Command to run the FastAPI application
CMD ["uvicorn", "backend.app.main:app", "--workers", "4", "--host", "0.0.0.0", "--port", "8000"]
