#!/bin/bash

# Function to print messages
log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1"
}

# Get the directory of the current script
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Step 1: Pull the latest source code from the main branch
log "Pulling latest source code from main branch..."
git -C "$SCRIPT_DIR" pull origin main || { log "Failed to pull from main branch"; exit 1; }

# Step 2: Bring the container down
log "Bringing down existing containers..."
docker compose -f "$SCRIPT_DIR/../docker-compose.yaml" down || { log "Failed to bring down containers"; exit 1; }

# Step 3: Build the new image
log "Building new image..."
docker compose -f "$SCRIPT_DIR/../docker-compose.yaml" build || { log "Failed to build new image"; exit 1; }

# Step 4: Sanitize (remove) old images
log "Sanitizing old images..."
docker image prune -f || { log "Failed to prune old images"; exit 1; }

# Step 5: Bring up the new container
log "Bringing up new container..."
docker compose -f "$SCRIPT_DIR/../docker-compose.yaml" up -d || { log "Failed to bring up new container"; exit 1; }

log "Deployment completed successfully."
