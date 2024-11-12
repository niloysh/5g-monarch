#!/bin/bash

# Variables
SERVICE_NAME="nfv_orchestrator"
USER="$(whoami)"
WORKING_DIR="$(pwd)"
SCRIPT_NAME="nfv-orchestrator.py"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
PYTHON_PATH="$(which python3)"

# Check if Python is installed
if [ -z "$PYTHON_PATH" ]; then
    echo "Python3 is not installed. Please install it and try again."
    exit 1
fi

# Create the service file
echo "Creating systemd service file at ${SERVICE_FILE}..."

sudo bash -c "cat > ${SERVICE_FILE}" <<EOL
[Unit]
Description=NFV Orchestrator Service
After=network.target

[Service]
User=${USER}
WorkingDirectory=${WORKING_DIR}
ExecStart=${PYTHON_PATH} ${WORKING_DIR}/${SCRIPT_NAME}
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd, start the service, and enable it to start on boot
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Starting the ${SERVICE_NAME} service..."
sudo systemctl start ${SERVICE_NAME}

echo "Enabling the ${SERVICE_NAME} service to start on boot..."
sudo systemctl enable ${SERVICE_NAME}

# Check the status of the service
echo "Checking the ${SERVICE_NAME} service status..."
sudo systemctl status ${SERVICE_NAME} --no-pager