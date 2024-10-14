#!/bin/bash

# Default values
DOCKERHUB_USERNAME=""
DOCKERHUB_PASSWORD=""
IMAGE_NAME=""
TAG="latest"

# Print usage function
usage() {
    echo "Usage: $0 -u <dockerhub-username> -p <dockerhub-password> -i <image-name> -t <tag>"
    echo "  -u, --username      Docker Hub username"
    echo "  -p, --password      Docker Hub password"
    echo "  -f, --file-path     Caminho para o arquivo docker-compose.yaml"
    echo "  -i, --image-name    Docker image name"
    echo "  -t, --tag           Docker image tag (default: latest)"
    exit 1
}

# Exit on error
set -e

# Parse command-line arguments using getopt
OPTS=$(getopt -o u:p:f:i:t: --long username:,password:,image-name:,tag: -n 'parse-options' -- "$@")
if [ $? != 0 ]; then
    usage
fi

eval set -- "$OPTS"

while true; do
    case "$1" in
    -u | --username )    DOCKERHUB_USERNAME="$2"; shift 2 ;;
    -p | --password )    DOCKERHUB_PASSWORD="$2"; shift 2 ;;
    -f | --dockerfile )    DOCKERFILE="$2"; shift 2 ;;
    -i | --image-name )  IMAGE_NAME="$2"; shift 2 ;;
    -t | --tag )         TAG="$2"; shift 2 ;;
    -- ) shift; break ;;
    * ) break ;;
    esac
done

# Validate required arguments
if [ -z "$DOCKERHUB_USERNAME" ]; then
    echo "Error: Docker Hub username is required."
    usage
fi

if [ -z "$DOCKERHUB_PASSWORD" ]; then
    echo "Error: Docker Hub password is required."
    usage
fi

if [ -z "$IMAGE_NAME" ]; then
    echo "Error: Docker image name is required."
    usage
fi


# Docker login
echo "[1] Logging in to Docker Hub..." 
echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin 
if [ $? -ne 0 ]; then
    echo "Docker login failed. Please check your credentials."
    exit 1
fi

# Build the Docker image
echo "[2] Building the Docker image..."
docker build -t "$IMAGE_NAME" "$DOCKERFILE"

# Tag the Docker image
echo "[3] Tagging the Docker image..."
docker tag $IMAGE_NAME $DOCKERHUB_USERNAME/$IMAGE_NAME:$TAG

# Push the Docker image to Docker Hub
echo "[4] Pushing the Docker image to Docker Hub..."
docker push $DOCKERHUB_USERNAME/$IMAGE_NAME:$TAG

# Check if the push was successful
if [ $? -eq 0 ]; then
    echo "Docker image pushed successfully!"
else
    echo "Failed to push the Docker image."
    exit 1
fi
