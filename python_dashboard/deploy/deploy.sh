#!/bin/bash
set -e

# Configuration
REMOTE_USER="hernando"
REMOTE_HOST="192.168.40.244"
REMOTE_PATH="/var/www/carnaval"
SERVICE_NAME="dashboard"

echo "🚀 Starting deployment..."

# Build/prepare locally if needed
echo "📦 Preparing deployment package..."

# Sync code to server
echo "📤 Syncing code to server..."
rsync -avz --delete \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.venv' \
    --exclude='node_modules' \
    ../ ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/python_dashboard/

# Run remote commands
echo "🔧 Setting up on server..."
ssh ${REMOTE_USER}@${REMOTE_HOST} << 'ENDSSH'
set -e

cd /var/www/carnaval/python_dashboard

# Create virtual environment if it doesn't exist
if [ ! -d "../.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv ../.venv
fi

# Activate and install dependencies
echo "Installing dependencies..."
source ../.venv/bin/activate
pip install --upgrade pip
pip install flask flask-socketio flask-cors requests python-dotenv

# Set correct permissions
echo "Setting permissions..."
sudo chown -R www-data:www-data /var/www/carnaval
sudo chmod -R 755 /var/www/carnaval

# Copy and enable systemd service
if [ -f "deploy/dashboard.service" ]; then
    echo "Installing systemd service..."
    sudo cp deploy/dashboard.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable dashboard
    sudo systemctl restart dashboard
    echo "✅ Service restarted"
fi

# Check service status
sudo systemctl status dashboard --no-pager

ENDSSH

echo "✅ Deployment complete!"
echo "📊 Check status: ssh ${REMOTE_USER}@${REMOTE_HOST} 'sudo systemctl status dashboard'"
