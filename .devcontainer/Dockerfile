# Use the official Python 3.13 image as base
FROM mcr.microsoft.com/devcontainers/python:3.13

# Install additional system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    git \
    vim \
    tree \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy requirements and install Python packages
COPY src/requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip==25.2 && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Set environment variables
ENV PYTHONPATH=/workspace/src
ENV PYTHONUNBUFFERED=1

# Create necessary directories
RUN mkdir -p /workspace/logs /workspace/data