#!/bin/bash

set -euo pipefail

# Copy .env.template to .env
cp .env.template .env

update_env_file() {
    local key="$1"
    local value="$2"
    local env_file=".env"

    # Ensure .env exists
    touch "$env_file"

    # Escape forward slashes and ampersands for sed compatibility
    escaped_value=$(printf '%s\n' "$value" | sed -e 's/[\&/]/\\&/g')

    # Use sed to replace the value if the key exists; otherwise, append
    if grep -q "^${key}=" "$env_file"; then
    sed -i.bak "s|^${key}=.*|${key}=${escaped_value}|" "$env_file" && rm -f "${env_file}.bak"
    else
    echo "${key}=${value}" >> "$env_file"
    fi
}

# List of keys to substitute
keys=(
    ENVIRONMENT
    POSTGRES_HOST
    POSTGRES_PORT
    POSTGRES_USER
    POSTGRES_PASSWORD
    JWT_SECRET_KEY
)

# Iterate and apply substitution based on actual environment variables
for key in "${keys[@]}"; do
    value="${!key:-}"
    if [[ -z "$value" ]]; then
        echo "Warning: Environment variable '$key' is not set." >&2
        continue
    fi
    update_env_file "$key" "$value"
done

echo ".env file successfully created and updated."
