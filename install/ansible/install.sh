#!/bin/bash

# Jukeberry Ansible Installation Script

# --- Helper Functions ---
echo_green() {
    echo -e "\033[0;32m$1\033[0m"
}

echo_error() {
    echo -e "\033[0;31mERROR: $1\033[0m"
}

# --- Main Script ---

# 1. Check for Ansible
echo_green "Checking for Ansible..."
if ! command -v ansible-playbook &> /dev/null; then
    echo_error "Ansible is not installed. Please install it before running this script."
    echo "See: https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html"
    exit 1
fi

# 2. Gather configuration from user
echo_green "--- Jukeberry Ansible Configuration ---"
read -p "Enter the IP address or hostname of your target machine: " TARGET_HOST
if [ -z "${TARGET_HOST}" ]; then
    echo_error "Target host cannot be empty."
    exit 1
fi

read -p "Enter the SSH user for the target machine [pi]: " ANSIBLE_USER
ANSIBLE_USER=${ANSIBLE_USER:-pi}

read -p "Enter the path to your music library [/var/media/music]: " MUSIC_LIB
MUSIC_LIB=${MUSIC_LIB:-/var/media/music}

read -p "Enable USB auto-mounting? (y/n) [n]: " AUTOMOUNT_USB_CHOICE
AUTOMOUNT_USB=false
if [[ "${AUTOMOUNT_USB_CHOICE}" =~ ^[Yy]$ ]]; then
    AUTOMOUNT_USB=true
fi

# 3. Create a temporary inventory file
echo_green "Creating temporary Ansible inventory..."
INVENTORY_FILE=$(mktemp)
cat << EOF > "${INVENTORY_FILE}"
[jukeberry_servers]
${TARGET_HOST} ansible_user=${ANSIBLE_USER}
EOF

# 4. Create a playbook to run
echo_green "Creating temporary Ansible playbook..."
PLAYBOOK_FILE=$(mktemp)
cat << EOF > "${PLAYBOOK_FILE}"
- hosts: jukeberry_servers
  become: true
  roles:
    - role: jukeberry
      music_library_path: "${MUSIC_LIB}"
      jukeberry_automount_usb: ${AUTOMOUNT_USB}
EOF

# 5. Run the playbook
echo_green "Running Ansible playbook..."
echo "This may take a few minutes. You may be prompted for the SSH and sudo password."
ansible-playbook -i "${INVENTORY_FILE}" "${PLAYBOOK_FILE}" --ask-become-pass

if [ $? -ne 0 ]; then
    echo_error "Ansible playbook failed."
else
    echo_green "Jukeberry installation complete!"
fi

# 6. Clean up temporary files
rm "${INVENTORY_FILE}"
rm "${PLAYBOOK_FILE}"
