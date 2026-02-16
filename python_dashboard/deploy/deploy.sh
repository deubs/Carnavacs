#!/bin/bash
# On-server deploy script for the Carnaval Dashboard
# Run this on 192.168.40.244 (the dashboard server)
set -e

REPO_PATH="/var/www/carnaval"
BRANCH="main"
SERVICE="dashboard"

cd "$REPO_PATH"

echo "Pulling latest changes..."
git pull origin "$BRANCH"

echo "Installing dependencies..."
.venv/bin/pip install -r python_dashboard/requirements.txt

echo "Updating systemd service..."
#sudo cp python_dashboard/deploy/dashboard.service /etc/systemd/system/
#sudo systemctl daemon-reload

echo "Restarting service..."
sudo systemctl restart "$SERVICE"

sleep 2

if sudo systemctl is-active --quiet "$SERVICE"; then
    echo "OK: $SERVICE is running"
    sudo systemctl status "$SERVICE" --no-pager
else
    echo "FAIL: $SERVICE is not running"
    sudo journalctl -u "$SERVICE" -n 20 --no-pager
    exit 1
fi
