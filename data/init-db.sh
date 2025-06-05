#!/bin/bash
set -e

echo "Waiting for database to be ready..."

until pg_isready -h db -p 5432 -U "$POSTGRES_USER"; do
    echo "Waiting for PostgreSQL..."
    sleep 2
done

echo "$POSTGRES_USER"
echo "$POSTGRES_DB"

echo "Database is up! Running SQL script..."
PGPASSWORD="$POSTGRES_PASSWORD" psql -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /data/sample_data.sql

