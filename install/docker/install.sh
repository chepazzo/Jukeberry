#!/bin/bash

# Jukeberry Docker Installation Script

# --- Helper Functions ---
echo_green() {
    echo -e "\033[0;32m$1\033[0m"
}

echo_error() {
    echo -e "\033[0;31mERROR: $1\033[0m"
}

# --- Main Script ---

# 1. Check for Docker and Docker Compose
echo_green "Checking for Docker and Docker Compose..."
if ! command -v docker &> /dev/null; then
    echo_error "Docker is not installed. Please install it before running this script."
    exit 1
fi

# Check for docker compose (v2) support
if ! docker compose version &> /dev/null; then
    echo_error "Docker Compose (v2) is not available. Please install Docker Compose v2 or later."
    exit 1
fi

# 2. Gather configuration from user
echo_green "--- Jukeberry Docker Configuration ---"
read -p "Enter the absolute path for your music library [$(pwd)/music]: " MUSIC_DIR
MUSIC_DIR=${MUSIC_DIR:-$(pwd)/music}

read -p "Enter the absolute path for your configuration directory [$(pwd)/config]: " CONFIG_DIR
CONFIG_DIR=${CONFIG_DIR:-$(pwd)/config}

read -p "Enter the container port [5000]: " CONTAINER_PORT
CONTAINER_PORT=${CONTAINER_PORT:-5000}

#read -p "Enter the audio player to use (e.g., mpg123, mpv) [mpg123]: " PLAYER
#PLAYER=${PLAYER:-mpg123}
PLAYER=mpg123

read -p "Enable USB auto-mounting within the container? (y/n) [n]: " AUTOMOUNT_USB_CHOICE
AUTOMOUNT_USB=false
if [[ "${AUTOMOUNT_USB_CHOICE}" =~ ^[Yy]$ ]]; then
    AUTOMOUNT_USB=true
fi

# 3. Create directories and generate config from template
echo_green "Creating directories and configuration file..."
mkdir -p "${MUSIC_DIR}"
mkdir -p "${CONFIG_DIR}"

# Generate jukeberry.conf from template
if [ -f "jukeberry.conf.j2" ]; then
    sed -e "s/{{ PORT }}/${CONTAINER_PORT}/g" \
        -e "s/{{ PLAYER }}/${PLAYER}/g" \
        jukeberry.conf.j2 > "${CONFIG_DIR}/jukeberry.conf"
    echo "Configuration file created at ${CONFIG_DIR}/jukeberry.conf"
else
    echo_error "jukeberry.conf.j2 template not found!"
    exit 1
fi

# 4. Create docker-compose.yml from template
echo_green "Creating docker-compose.yml..."
if [ -f "docker-compose.yml.j2" ]; then
    sed -e "s|{{ CONTAINER_PORT }}|${CONTAINER_PORT}|g" \
        -e "s|{{ MUSIC_DIR }}|${MUSIC_DIR}|g" \
        -e "s|{{ CONFIG_DIR }}|${CONFIG_DIR}|g" \
        docker-compose.yml.j2 > "docker-compose.yml"
    echo "docker-compose.yml created successfully."
else
    echo_error "docker-compose.yml.j2 template not found!"
    exit 1
fi

if [ "${AUTOMOUNT_USB}" = true ]; then
cat << EOF >> "docker-compose.yml"
    privileged: true
    volumes:
      - /dev:/dev
      - /run/udev:/run/udev:ro
EOF
fi

# 5. Build and start the container
echo_green "Building and starting the Jukeberry container..."
echo "This may take a few minutes."
docker compose up --build -d

if [ $? -ne 0 ]; then
    echo_error "Docker Compose failed to build and start the container."
else
    echo_green "Jukeberry installation complete!"
    echo_green "The container is running in the background."
    echo_green "You can access the application at http://localhost:5000"
fi

