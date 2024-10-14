#!/bin/bash

# Default values
PORTAINER_URL=""
USERNAME=""
PASSWORD=""
STACK_NAME=""

# Print usage function
usage() {
    echo "Usage: $0 -url <portainer-url> -u <username> -p <password> -s <stack-name>"
    echo "  -r, --url         URL do Portainer"
    echo "  -u, --username     Portainer username"
    echo "  -p, --password     Portainer password"
    echo "  -s, --stack-name   Stack name to be removed"
    exit 1
}

# Exit on error
set -e

# Parse command-line arguments using getopt
OPTS=$(getopt -o r:u:p:s: --long url:,username:,password:,stack-name: -n 'parse-options' -- "$@")
if [ $? != 0 ]; then
    usage
fi

eval set -- "$OPTS"

while true; do
    case "$1" in
    -r | --url )          PORTAINER_URL="$2"; shift 2 ;;
    -u | --username )     USERNAME="$2"; shift 2 ;;
    -p | --password )     PASSWORD="$2"; shift 2 ;;
    -s | --stack-name )   STACK_NAME="$2"; shift 2 ;;
    -- ) shift; break ;;
    * ) break ;;
    esac
done

# Validate required arguments
if [ -z "$PORTAINER_URL" ]; then
    echo "Error: Portainer URL is required."
    usage
fi

if [ -z "$USERNAME" ]; then
    echo "Error: Username is required."
    usage
fi

if [ -z "$PASSWORD" ]; then
    echo "Error: Password is required."
    usage
fi

if [ -z "$STACK_NAME" ]; then
    echo "Error: Stack name is required."
    usage
fi

# Install jq if not installed
if ! command -v jq &> /dev/null; then
    echo "Installing jq..."
    sudo apt-get install jq -y > /dev/null 2>&1 || { echo "Failed to install jq. Exiting."; exit 1; }
    echo "jq installed successfully."
fi

# Function to handle errors
handle_error() {
    echo "Error: $1"
    exit 1
}

# Step 1: Get JWT authentication token
echo "[1] Authenticating with Portainer..."
TOKEN_RESPONSE=$(curl -k -s -X POST -H "Content-Type: application/json" \
            -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" \
            "https://$PORTAINER_URL/api/auth")

# Extract token from the response
JWT_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.jwt')

if [ "$JWT_TOKEN" == "null" ] || [ -z "$JWT_TOKEN" ]; then
    handle_error "Failed to authenticate. Check your username and password."
fi

echo "Authenticated successfully. Token retrieved."

# Step 2: Get the stack ID by name
echo "[2] Retrieving stack ID for stack: ${STACK_NAME}..."
STACK_ID=$(curl -s -X GET "https://${PORTAINER_URL}/api/stacks" \
    -H "Authorization: Bearer ${JWT_TOKEN}" \
    -H "Content-Type: application/json" | \
    jq -r ".[] | select(.Name==\"${STACK_NAME}\") | .Id")

# If stack doesn't exist, exit the script without error
if [ -z "$STACK_ID" ]; then
    echo "Stack not found: ${STACK_NAME}. Exiting without error."
    exit 0
fi

echo "Stack ID for ${STACK_NAME} is ${STACK_ID}"

# Step 2.5: Get the endpoint ID
GET_RESPONSE=$(curl -s -X GET "https://${PORTAINER_URL}/api/stacks/${STACK_ID}" \
    -H "Authorization: Bearer ${JWT_TOKEN}" \
    -H "Content-Type: application/json")

ENDPOINT_ID=$(echo "$GET_RESPONSE" | jq -r '.EndpointId')

if [ -z "$ENDPOINT_ID" ]; then
    handle_error "Failed to retrieve Endpoint ID for stack."
fi

echo "Endpoint ID for the stack is ${ENDPOINT_ID}"

# Step 3: Remove the stack by ID and endpoint ID
echo "[3] Removing stack: ${STACK_NAME}..."
DELETE_RESPONSE=$(curl -s -X DELETE "https://${PORTAINER_URL}/api/stacks/${STACK_ID}?endpointId=${ENDPOINT_ID}" \
    -H "Authorization: Bearer ${JWT_TOKEN}" \
    -H "Content-Type: application/json")

if [ -z "$DELETE_RESPONSE" ]; then
    echo "Stack ${STACK_NAME} removed successfully."
else
    handle_error "Failed to remove stack. Response: ${DELETE_RESPONSE}"
fi
