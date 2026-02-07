#!/bin/bash
# Alternative deployment using git on the server

set -e

REMOTE_USER="your_user"
REMOTE_HOST="your_server_ip"
REPO_PATH="/var/www/carnaval"
BRANCH="main"

echo "🚀 Deploying via git pull..."

ssh ${REMOTE_USER}@${REMOTE_HOST} << ENDSSH
set -e

cd ${REPO_PATH}

# Stash any local changes
git stash

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin ${BRANCH}

# Activate virtual environment and update dependencies
echo "📦 Updating dependencies..."
source .venv/bin/activate
pip install -r python_dashboard/requirements.txt 2>/dev/null || echo "No requirements.txt found"

# Restart service
echo "🔄 Restarting service..."
sudo systemctl restart dashboard

# Check status
sudo systemctl status dashboard --no-pager

# Show recent logs
echo ""
echo "📋 Recent logs:"
sudo journalctl -u dashboard -n 20 --no-pager

ENDSSH

echo "✅ Deployment complete!"
