# Deployment Guide

## Initial Server Setup

1. **On the Debian server**, run the setup script:
   ```bash
   bash setup-server.sh
   ```

2. **Edit configuration files**:
   - Update `dashboard.service` with correct user/paths if needed
   - Update `nginx.conf` with your domain name
   - Update deploy scripts with your server IP and username

## Deployment Methods

### Method 1: Rsync Deploy (Recommended for development)

This method syncs your local code to the server.

1. Edit `deploy.sh` and set:
   ```bash
   REMOTE_USER="your_username"
   REMOTE_HOST="192.168.40.227"  # your server IP
   ```

2. Make executable and run:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

### Method 2: Git Deploy (Recommended for production)

This method uses git on the server to pull changes.

1. **On the server**, initialize git repository:
   ```bash
   cd /var/www/carnaval
   git init
   git remote add origin <your-repo-url>
   git pull origin main
   ```

2. **From your local machine**, edit `git-deploy.sh` and set:
   ```bash
   REMOTE_USER="your_username"
   REMOTE_HOST="192.168.40.227"
   ```

3. Make executable and run:
   ```bash
   chmod +x git-deploy.sh
   ./git-deploy.sh
   ```

## Managing the Service

```bash
# Start service
sudo systemctl start dashboard

# Stop service
sudo systemctl stop dashboard

# Restart service
sudo systemctl restart dashboard

# Check status
sudo systemctl status dashboard

# View logs
sudo journalctl -u dashboard -f

# View recent logs
sudo journalctl -u dashboard -n 50
```

## Nginx Commands

```bash
# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# Restart nginx
sudo systemctl restart nginx

# Check nginx status
sudo systemctl status nginx
```

## SSL Certificate (Optional)

Install Let's Encrypt certificate:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d dashboard.carnavaldelpais.com.ar
```

## Troubleshooting

### Service won't start
```bash
# Check logs
sudo journalctl -u dashboard -xe

# Check if port is already in use
sudo netstat -tlnp | grep :5000

# Test running manually
cd /var/www/carnaval/python_dashboard/api_server
/var/www/carnaval/.venv/bin/python api_server.py
```

### Nginx shows 502 Bad Gateway
```bash
# Check if dashboard service is running
sudo systemctl status dashboard

# Check nginx error log
sudo tail -f /var/log/nginx/error.log
```

### Permission denied errors
```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/carnaval

# Fix permissions
sudo chmod -R 755 /var/www/carnaval
```

## Quick Deploy Command

Add to your `.bashrc` or `.zshrc`:
```bash
alias deploy-dashboard='cd ~/trabajo/carnaval/src/python_dashboard/deploy && ./deploy.sh'
```

Then just run:
```bash
deploy-dashboard
```
