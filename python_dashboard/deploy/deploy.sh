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

# Sync code to server (entire repository)
echo "📤 Syncing code to server..."
rsync -avz --delete \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.venv' \
    --exclude='node_modules' \
    --exclude='.vscode' \
    ../../ ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/

# Run remote commands
echo "🔧 Setting up on server..."
ssh ${REMOTE_USER}@${REMOTE_HOST} << 'ENDSSH'
set -e

cd /var/www/carnaval

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate and install dependencies
echo "Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip
if [ -f "python_dashboard/requirements.txt" ]; then
    pip install -r python_dashboard/requirements.txt
else
    pip install flask flask-socketio flask-cors requests python-dotenv
fi

# Set correct permissions
echo "Setting permissions..."
sudo chowpython_dashboard/deploy/dashboard.service" ]; then
    echo "Installing systemd service..."
    sudo cp python_dashboard/
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
