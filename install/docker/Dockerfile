# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies (git for cloning, mpg321 for playback)
RUN apt-get update && apt-get install -y git mpg321 --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy the application source code into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables for configuration
ENV PLAYER=mpg321
ENV MUSIC_LIBRARY=/music
ENV CONFIG_PATH=/config/jukeberry.conf

# Create a default config file
RUN mkdir /config
RUN echo "[jukeberry]\nplayer = ${PLAYER}\nlibrary = ${MUSIC_LIBRARY}" > ${CONFIG_PATH}

# Run the application
CMD ["python3", "-m", "jukeberry.server", "--config", "/config/jukeberry.conf"]
