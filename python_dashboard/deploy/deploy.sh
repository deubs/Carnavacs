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

# Set correct permissions (if we have sudo)
echo "Setting permissions..."
if sudo -n true 2>/dev/null; then
    sudo chown -R www-data:www-data /var/www/carnaval 2>/dev/null || {
        echo "Cannot change ownership to www-data, keeping current user"
    }
    sudo chmod -R 755 /var/www/carnaval
else
    chmod -R 755 /var/www/carnaval 2>/dev/null || echo "Skipping permission changes"
fi

# Copy and enable systemd service (if we have sudo)
if [ -f "python_dashboard/deploy/dashboard.service" ]; then
    if sudo -n true 2>/dev/null; then
        echo "Installing systemd service..."
        sudo cp python_dashboard/deploy/dashboard.service /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable dashboard
        sudo systemctl restart dashboard
        echo "✅ Service restarted via systemd"
    else
        echo "⚠️  Cannot install systemd service (no sudo access)"
        echo "Restarting manually..."
        pkill -f "python.*api_server.py" 2>/dev/null || true
        sleep 2
        cd python_dashboard/api_server
        nohup ../../.venv/bin/python api_server.py > ../../dashboard.log 2>&1 &
        echo "✅ Service restarted manually (PID: $!)"
        cd ../..
    fi
fi

# Check service status
if sudo -n true 2>/dev/null; then
    sudo systemctl status dashboard --no-pager || true
else
    echo ""
    echo "📋 Service is running. To check logs:"
    echo "   tail -f /var/www/carnaval/dashboard.log"
    echo ""
    echo "Recent logs:"
    tail -n 20 /var/www/carnaval/dashboard.log 2>/dev/null || echo "No logs yet"
fi

ENDSSH

echo ""
echo "✅ Deployment complete!"
echo ""
if ssh ${REMOTE_USER}@${REMOTE_HOST} "sudo -n true 2>/dev/null"; then
    echo "📊 Check status: ssh ${REMOTE_USER}@${REMOTE_HOST} 'sudo systemctl status dashboard'"
else
    echo "📊 Check logs: ssh ${REMOTE_USER}@${REMOTE_HOST} 'tail -f /var/www/carnaval/dashboard.log'"
fi
