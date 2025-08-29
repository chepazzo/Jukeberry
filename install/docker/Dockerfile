# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies (git, player, and tools for USB automount)
RUN apt-get update && apt-get install -y git mpg321 udisks2 udev --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy the application source code into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy udev rule for USB automounting
COPY install/docker/99-usb-mount.rules /etc/udev/rules.d/99-usb-mount.rules

# Copy and set up the start script
COPY install/docker/start.sh /start.sh
RUN chmod +x /start.sh

# Make port 5000 available
EXPOSE 5000

# Define environment variables for configuration
ENV PLAYER=mpg321
ENV MUSIC_LIBRARY=/music

# Create a default config file if one isn't mounted
RUN mkdir -p /config
RUN echo "[jukeberry]\nplayer = ${PLAYER}\nlibrary = ${MUSIC_LIBRARY}" > /config/jukeberry.conf

# Set the entrypoint to our start script
ENTRYPOINT ["/start.sh"]
