# Default values
$DOCKERHUB_USERNAME = ""
$DOCKERHUB_PASSWORD = ""
$IMAGE_NAME = "conexxohub-site"
$TAG = "latest"

# Print usage function
function usage {
    Write-Host "Usage: script.ps1 -username <dockerhub-username> -password <dockerhub-password> -image-name <image-name> -tag <tag>"
    Write-Host "  -username   Docker Hub username"
    Write-Host "  -password   Docker Hub password"
    Write-Host "  -image-name Docker image name (default: conexxohub-site)"
    Write-Host "  -tag        Docker image tag (default: latest)"
    exit 1
}

# Parse command-line arguments
param (
    [Parameter(Mandatory=$true)][string]$username,
    [Parameter(Mandatory=$true)][string]$password,
    [string]$imageName = "conexxohub-site",
    [string]$tag = "latest"
)

# Assigning parameters
$DOCKERHUB_USERNAME = $username
$DOCKERHUB_PASSWORD = $password
$IMAGE_NAME = $imageName
$TAG = $tag

# Docker login
Write-Host "[1] Logging in to Docker Hub..."
echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker login failed. Please check your credentials."
    exit 1
}

# Build the Docker image
Write-Host "[2] Building the Docker image..."
docker build -t $IMAGE_NAME .

# Tag the Docker image
Write-Host "[3] Tagging the Docker image..."
docker tag $IMAGE_NAME "$DOCKERHUB_USERNAME/$IMAGE_NAME:$TAG"
docker tag $IMAGE_NAME "brunolnetto1234/$IMAGE_NAME:latest"

# Push the Docker image to Docker Hub
Write-Host "[4] Pushing the Docker image to Docker Hub..."
docker push "$DOCKERHUB_USERNAME/$IMAGE_NAME:$TAG"
docker push "brunolnetto1234/$IMAGE_NAME:latest"

# Check if the push was successful
if ($LASTEXITCODE -eq 0) {
    Write-Host "Docker image pushed successfully!"
} else {
    Write-Host "Failed to push the Docker image."
    exit 1
}
