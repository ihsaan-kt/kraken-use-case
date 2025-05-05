#!/bin/bash

# Check if Docker is installed/running
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not found. Please install Docker Desktop for macOS:"
    echo "https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "ERROR: Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

# Start Kafka and pipeline
echo "Starting Kafka and pipeline..."
docker compose up --build --force-recreate