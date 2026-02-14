# Dashboard Deployment

Server: 192.168.40.244 (Debian, nginx)

## Architecture

```
client -> nginx (:80) -> eventlet (:5000) -> Flask+SocketIO
```

Flask-SocketIO auto-detects eventlet and uses its production WSGI server.

## Deploy

SSH into the server and run:

```bash
cd /var/www/carnaval
bash python_dashboard/deploy/deploy.sh
```

This pulls from git, installs dependencies, updates the systemd service, and restarts.

## Manual Commands

```bash
# Status
sudo systemctl status dashboard

# Restart
sudo systemctl restart dashboard

# Logs (follow)
sudo journalctl -u dashboard -f

# Recent logs
sudo journalctl -u dashboard -n 50

# Test endpoint
curl http://localhost:5000/fps
```

## Nginx

```bash
sudo nginx -t                    # test config
sudo systemctl reload nginx      # reload
```

Config: `/etc/nginx/sites-available/dashboard`

## Files

| File | Purpose |
|------|---------|
| `deploy.sh` | On-server deploy script |
| `dashboard.service` | systemd unit (eventlet) |
| `nginx.conf` | nginx reverse proxy config |
| `firewall-nftables.sh` | nftables firewall rules |
