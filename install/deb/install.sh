#!/bin/bash

# Jukeberry Installation Script for Debian-based systems

# --- Configuration ---
DEFAULT_JUKEBERRY_USER="pi"
DEFAULT_INSTALL_DIR="/opt/jukeberry"
DEFAULT_PLAYER="mpg321"
DEFAULT_MUSIC_LIB="/var/media/music"
GITHUB_REPO="https://github.com/chepazzo/jukeberry.git"

# --- Helper Functions ---
echo_green() {
    echo -e "\033[0;32m$1\033[0m"
}

echo_error() {
    echo -e "\033[0;31mERROR: $1\033[0m"
}

# --- Main Script ---

# 1. Check for root privileges
echo_green "Checking for root privileges..."
if [[ $EUID -ne 0 ]]; then
   echo_error "This script must be run as root. Please use sudo."
   exit 1
fi

# 2. Gather configuration from user
echo_green "--- Jukeberry Configuration ---"
read -p "Enter the user to run Jukeberry as [${DEFAULT_JUKEBERRY_USER}]: " JUKEBERRY_USER
JUKEBERRY_USER=${JUKEBERRY_USER:-$DEFAULT_JUKEBERRY_USER}

read -p "Enter the installation directory [${DEFAULT_INSTALL_DIR}]: " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-$DEFAULT_INSTALL_DIR}

read -p "Enter the music player to use (mpg321 or omxplayer) [${DEFAULT_PLAYER}]: " PLAYER
PLAYER=${PLAYER:-$DEFAULT_PLAYER}

read -p "Enter the path to your music library [${DEFAULT_MUSIC_LIB}]: " MUSIC_LIB
MUSIC_LIB=${MUSIC_LIB:-$DEFAULT_MUSIC_LIB}

CONFIG_FILE="/etc/jukeberry.conf"

# 3. Install system dependencies
echo_green "Installing system dependencies..."
apt-get update
apt-get install -y python3 python3-pip git "${PLAYER}"
if [ $? -ne 0 ]; then
    echo_error "Failed to install system dependencies."
    exit 1
fi

# 4. Create user and directories
echo_green "Creating user and directories..."
id -u "${JUKEBERRY_USER}" &>/dev/null || useradd -m "${JUKEBERRY_USER}"
mkdir -p "${INSTALL_DIR}"
mkdir -p "${MUSIC_LIB}"
chown -R "${JUKEBERRY_USER}:${JUKEBERRY_USER}" "${INSTALL_DIR}"
chown -R "${JUKEBERRY_USER}:${JUKEBERRY_USER}" "${MUSIC_LIB}"

# 5. Clone the repository
echo_green "Cloning Jukeberry repository to ${INSTALL_DIR}..."
su - "${JUKEBERRY_USER}" -c "git clone ${GITHUB_REPO} ${INSTALL_DIR}"
if [ $? -ne 0 ]; then
    echo_error "Failed to clone the repository."
    exit 1
fi

# 6. Install Python dependencies
echo_green "Installing Python dependencies..."
su - "${JUKEBERRY_USER}" -c "pip3 install -r ${INSTALL_DIR}/requirements.txt"
if [ $? -ne 0 ]; then
    echo_error "Failed to install Python dependencies."
    exit 1
fi

# 7. Create the configuration file
echo_green "Creating configuration file at ${CONFIG_FILE}..."
cat << EOF > "${CONFIG_FILE}"
[jukeberry]
player = ${PLAYER}
library = ${MUSIC_LIB}
EOF

# 8. Create the systemd service file
echo_green "Creating systemd service file..."
SERVICE_FILE="/etc/systemd/system/jukeberry.service"
cat << EOF > "${SERVICE_FILE}"
[Unit]
Description=Jukeberry Music Player
After=network.target

[Service]
User=${JUKEBERRY_USER}
Group=${JUKEBERRY_USER}
WorkingDirectory=${INSTALL_DIR}
ExecStart=/usr/bin/python3 -m jukeberry.server --config ${CONFIG_FILE}
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 9. Enable and start the service
echo_green "Enabling and starting the Jukeberry service..."
systemctl daemon-reload
systemctl enable jukeberry.service
systemctl start jukeberry.service

echo_green "Installation complete!"
echo_green "Jukeberry is running and will start automatically on boot."
echo_green "You can access it at http://<your-pi-ip>:5000"
