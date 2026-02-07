#!/bin/bash
# Configure firewall using nftables (default in Debian 11+)

echo "🔥 Configuring firewall with nftables..."

# Check if nftables is available
if ! command -v nft &> /dev/null; then
    echo "nftables not found. Installing..."
    sudo apt install -y nftables
fi

# Create basic firewall rules
sudo nft add table inet filter 2>/dev/null || true
sudo nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; } 2>/dev/null || true
sudo nft add chain inet filter forward { type filter hook forward priority 0 \; policy drop \; } 2>/dev/null || true
sudo nft add chain inet filter output { type filter hook output priority 0 \; policy accept \; } 2>/dev/null || true

# Allow established connections
sudo nft add rule inet filter input ct state established,related accept

# Allow loopback
sudo nft add rule inet filter input iif lo accept

# Allow SSH (be careful!)
sudo nft add rule inet filter input tcp dport 22 accept

# Allow HTTP and HTTPS
sudo nft add rule inet filter input tcp dport { 80, 443 } accept

# Allow dashboard port (optional, if not using nginx reverse proxy)
sudo nft add rule inet filter input tcp dport 5000 accept

# Save rules
sudo nft list ruleset > /etc/nftables.conf

# Enable nftables service
sudo systemctl enable nftables
sudo systemctl restart nftables

echo "✅ Firewall configured!"
echo "To view rules: sudo nft list ruleset"
echo "To disable: sudo systemctl stop nftables"
