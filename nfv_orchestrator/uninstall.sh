#!/bin/bash

SERVICE_NAME="nfv_orchestrator"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

# Check if the service file exists
if [ ! -f "$SERVICE_FILE" ]; then
    echo "Service file ${SERVICE_FILE} does not exist. Exiting."
    exit 1
fi

echo "Stopping the ${SERVICE_NAME} service..."
sudo systemctl stop "$SERVICE_NAME" || {
    echo "Failed to stop the ${SERVICE_NAME} service. Exiting."
    exit 1
}

echo "Disabling the ${SERVICE_NAME} service..."
sudo systemctl disable "$SERVICE_NAME" || {
    echo "Failed to disable the ${SERVICE_NAME} service. Exiting."
    exit 1
}

echo "Removing the service file at ${SERVICE_FILE}..."
sudo rm "$SERVICE_FILE" || {
    echo "Failed to remove the service file. Exiting."
    exit 1
}

echo "Reloading systemd daemon to apply changes..."
sudo systemctl daemon-reload

# Optional: Clean up logs
echo "Clearing systemd logs for ${SERVICE_NAME}..."
sudo journalctl --vacuum-files=1 -u "$SERVICE_NAME" &> /dev/null

# Verify removal
if ! systemctl status "$SERVICE_NAME" &> /dev/null; then
    echo "${SERVICE_NAME} service has been successfully removed."
else
    echo "Warning: ${SERVICE_NAME} service may still be present."
fi