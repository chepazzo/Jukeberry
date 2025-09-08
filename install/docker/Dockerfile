# Stage 1: Build the frontend assets
FROM node:18-slim as builder

WORKDIR /usr/src/app

# Copy frontend package management files
COPY frontend/package.json frontend/package-lock.json* ./frontend/

# Install frontend dependencies
RUN cd frontend && npm install --legacy-peer-deps

# Copy the rest of the frontend source code
COPY frontend/ ./frontend/

# Build the frontend
RUN cd frontend && npm run build

# --- 

# Stage 2: Build the final Python application image
FROM python:3.9-slim

WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y --fix-missing \
    git \
    mpg123 \
    mpg321 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application source code
COPY . .

# Copy the built frontend assets from the builder stage
COPY --from=builder /usr/src/app/frontend/dist ./frontend/dist

# Copy and set up the start script
COPY install/docker/start.sh /start.sh
RUN chmod +x /start.sh

# Set the entrypoint
ENTRYPOINT ["/start.sh"]