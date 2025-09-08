#!/bin/bash

# --- Start USB Automounting Services (if available) ---
UDEVD_PATH="/lib/systemd/systemd-udevd"
UDEVADM_PATH="/usr/bin/udevadm"

if [ -x "$UDEVD_PATH" ] && [ -x "$UDEVADM_PATH" ]; then
    echo "Starting udev services for USB automounting..."
    $UDEVD_PATH --daemon
    $UDEVADM_PATH trigger
else
    echo "udev services not found, skipping USB automounting setup."
fi

# --- Start the Jukeberry Server ---
echo "Starting Jukeberry server..."
python3 -m jukeberry.runserver -i /config/jukeberry.conf
