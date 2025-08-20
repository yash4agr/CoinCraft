# CoinCraft Backend Deployment Guide

## Prerequisites
- Ubuntu/Debian server with sudo access
- Domain `api.iitmquizzes.tech` pointing to your server IP
- Git repository cloned on your server

## Deployment Steps

### 1. Clone the repository (if not done already)
```bash
git clone https://github.com/vidhanm/coincraft.git
cd coincraft/backend
```

### 2. Make the deployment script executable
```bash
chmod +x deploy.sh
```

### 3. Run the deployment script
```bash
sudo ./deploy.sh
```

### 4. Verify deployment
```bash
# Check if service is running
sudo systemctl status coincraft

# Check logs
sudo journalctl -u coincraft -f

# Test API endpoint
curl https://api.iitmquizzes.tech/health
```

## Post-Deployment

### Update environment variables (if needed)
```bash
sudo nano /var/www/coincraft/backend/.env.production
sudo systemctl restart coincraft
```

### Update code from repository
```bash
cd /path/to/your/coincraft/backend
git pull
sudo cp -r ./* /var/www/coincraft/backend/
sudo systemctl restart coincraft
```

### SSL Certificate Renewal (automatic via certbot)
```bash
# Test renewal
sudo certbot renew --dry-run
```

## Troubleshooting

### Check service status
```bash
sudo systemctl status coincraft
```

### View logs
```bash
# Service logs
sudo journalctl -u coincraft -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Application logs
sudo tail -f /var/log/coincraft/error.log
```

### Restart services
```bash
sudo systemctl restart coincraft
sudo systemctl reload nginx
```

## Important Files Locations
- Application: `/var/www/coincraft/backend/`
- Service config: `/etc/systemd/system/coincraft.service`
- Nginx config: `/etc/nginx/sites-available/coincraft-api`
- Logs: `/var/log/coincraft/`
