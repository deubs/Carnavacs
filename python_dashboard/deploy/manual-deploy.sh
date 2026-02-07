#!/bin/bash
# Manual deployment script for users without sudo access

set -e

echo "🚀 Starting manual deployment (no sudo required)..."

cd ~/carnaval || cd /var/www/carnaval

# Pull latest changes
echo "📥 Pulling latest code..."
git pull

# Update dependencies
echo "📦 Installing dependencies..."
source .venv/bin/activate
pip install -r python_dashboard/requirements.txt

# Restart service manually
echo "🔄 Restarting service..."
pkill -f "python.*api_server.py" 2>/dev/null || echo "Service not running"
sleep 2

cd python_dashboard/api_server
nohup ../../.venv/bin/python api_server.py > ../../dashboard.log 2>&1 &
NEW_PID=$!

echo "✅ Service started (PID: $NEW_PID)"
echo ""
echo "📋 Useful commands:"
echo "  View logs: tail -f ~/carnaval/dashboard.log"
echo "  Check process: ps aux | grep api_server"
echo "  Stop service: pkill -f 'python.*api_server.py'"
