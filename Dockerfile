# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies required for Pygame/SDL
# We keep the image slim but need these for audio/video
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We don't COPY . . here because we will mount the volume in docker-compose
# This allows for hot-reloading (changing code without rebuilding image)

# Default command
CMD ["python", "src/main.py"]
