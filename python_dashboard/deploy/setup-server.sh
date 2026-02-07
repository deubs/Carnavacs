#!/bin/bash
# Run this script on the Debian server to set up initial environment

set -e

echo "🔧 Setting up Debian server for Carnaval Dashboard..."

# Update system
echo "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install required packages
echo "📦 Installing required packages..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    nginx \
    curl

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /var/www/carnaval
sudo chown -R $USER:$USER /var/www/carnaval

# Clone repository (if using git)
# cd /var/www/carnaval
# git clone <your-repo-url> .

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
cd /var/www/carnaval
python3 -m venv .venv
source .venv/bin/activate

# Install Python packages
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install flask flask-socketio flask-cors requests python-dotenv

# Configure nginx
echo "🌐 Configuring nginx..."
sudo cp python_dashboard/deploy/nginx.conf /etc/nginx/sites-available/dashboard
sudo ln -sf /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx

# Set up systemd service
echo "⚙️  Setting up systemd service..."
sudo cp python_dashboard/deploy/dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dashboard
sudo systemctl start dashboard

# Configure firewall (if using ufw)
echo "🔥 Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow 5000/tcp

echo "✅ Server setup complete!"
echo ""
echo "Next steps:"
echo "1. Update deploy/deploy.sh with your server details"
echo "2. Run deploy.sh from your local machine to deploy"
echo "3. Check service status: sudo systemctl status dashboard"
echo "4. View logs: sudo journalctl -u dashboard -f"
