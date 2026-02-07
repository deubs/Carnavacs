#!/bin/bash
# Run this script on the Debian server to set up initial environment

set -e

echo "🔧 Setting up Debian server for Carnaval Dashboard..."

# Check if we have sudo access
HAS_SUDO=false
if sudo -n true 2>/dev/null; then
    HAS_SUDO=true
    echo "✅ Running with sudo access"
else
    echo "⚠️  Running without sudo - some steps will be skipped"
    echo "    Ask your administrator to install: python3 python3-pip python3-venv git nginx"
fi

# Update system (if we have sudo)
if [ "$HAS_SUDO" = true ]; then
    echo "📦 Updating system packages..."
    sudo apt update
    sudo apt upgrade -y
    
    # Install required packages
mkdir -p /var/www/carnaval 2>/dev/null || {
    echo "⚠️  Cannot create /var/www/carnaval - using ~/carnaval instead"
    mkdir -p ~/carnaval
    cd ~
    APP_DIR="$HOME/carnaval"
}

if [ -z "$APP_DIR" ]; then
    APP_DIR="/var/www/carnaval"
    cd /var/www
fi
        python3 \
        python3-pip \
        python3-venv \
        git \
        nginx \
        curl
else
    echo "⏭️  Skipping system package installation (requires sudo)"
if [ ! -d "carnaval/.git" ]; then
    echo "Enter your git repository URL (or press Enter to skip):"
    read REPO_URL
    if [ -n "$REPO_URL" ]; then
        git clone $REPO_URL carnaval
    fi
else
    echo "Repository already exists, pulling latest changes..."
    cd carnaval
    git pull
fi

cd $APP_DIR  echo "Enter your git repository URL (or press Enter to skip):"
    read REPO_URL
    if [ -n "$REPO_URL" ]; then
        git clone $REPO_URL carnaval
    fi
else
    echo "Repository already exists, pulling latest changes..."
    cd carnaval
    git pull
fi

# Create virtual environment
ecSystem service and nginx (requires sudo)
if [ "$HAS_SUDO" = true ]; then
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
    
    # Configure firewall (optional)
    echo "🔥 Configuring firewall..."
    if command -v ufw &> /dev/null; then
        echo "Using ufw..."
        sudo ufw allow 'Nginx Full'
        sudo ufw allow 5000/tcp
    else
        echo "UFW not found. Configure firewall manually if needed:"
        echo "  For nftables: sudo nft add rule inet filter input tcp dport { 80, 443, 5000 } accept"
        echo "  Or install ufw: sudo apt install ufw"
    fi
else
    echo "⚠️  Skipping nginx and systemd setup (requires sudo)"
    echo ""
    echo "📋 Manual steps needed (ask your administrator):"
    echo "1. Copy nginx config: sudo cp $APP_DIR/python_dashboard/deploy/nginx.conf /etc/nginx/sites-available/dashboard"
    echo "2. Enable site: sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/"
    echo "3. Restart nginx: sudo systemctl restart nginx"
    echo "4. Install service: sudo cp $APP_DIR/python_dashboard/deploy/dashboard.service /etc/systemd/system/"
    echo "5. Enable service: sudo systemctl enable --now dashboard"
    echo ""
    echo "Or run manually:"
    echo "  cd $APP_DIR/python_dashboard/api_server"
    echo "  $APP_DIR/.venv/bin/python api_server.py
# Configure firewall (optional)
echo "🔥 Configuring firewall..."
if command -v ufw &> /dev/null; then
    echo "Using ufw..."
    sudo ufw allow 'Nginx Full'
    sudo ufw allow 5000/tcp
else
    echo "UFW not found. Configure firewall manually if needed:"
    echo "  For nftables: sudo nft add rule inet filter input tcp dport { 80, 443, 5000 } accept"
    echo "  Or install ufw: sudo apt install ufw"
fi

echo "✅ Server setup complete!"
echo ""
echo "Next steps:"
echo "1. Update deploy/deploy.sh with your server details"
echo "2. Run deploy.sh from your local machine to deploy"
echo "3. Check service status: sudo systemctl status dashboard"
echo "4. View logs: sudo journalctl -u dashboard -f"
