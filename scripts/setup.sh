#!/bin/bash
# This script builds and starts the Docker services in detached mode.

echo "Starting Docker services..."
docker compose up --build -d
