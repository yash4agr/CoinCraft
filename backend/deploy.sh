#!/bin/bash
# CoinCraft Backend Deployment Script

set -e

echo "🚀 Starting CoinCraft Backend Deployment..."

# Variables
APP_DIR="/var/www/coincraft/backend"
SERVICE_NAME="coincraft"
NGINX_SITE="coincraft-api"

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo "🔧 Installing system dependencies..."
sudo apt install -y python3.12 python3-pip nginx certbot python3-certbot-nginx git

# Install uv package manager
echo "📦 Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p $APP_DIR
sudo mkdir -p /var/log/coincraft

# Clone repository (you'll need to do this manually)
echo "📥 Clone your repository to $APP_DIR"
echo "git clone https://github.com/vidhanm/coincraft.git /tmp/coincraft"
echo "sudo cp -r /tmp/coincraft/backend/* $APP_DIR/"

# Set permissions
echo "🔐 Setting permissions..."
sudo chown -R www-data:www-data $APP_DIR
sudo chown -R www-data:www-data /var/log/coincraft

# Setup Python environment
echo "🐍 Setting up Python environment..."
cd $APP_DIR
sudo -u www-data uv venv
sudo -u www-data .venv/bin/pip install -r requirements.txt

# Setup systemd service
echo "⚙️ Setting up systemd service..."
sudo cp coincraft.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

# Setup Nginx
echo "🌐 Setting up Nginx..."
sudo cp nginx-coincraft-api.conf /etc/nginx/sites-available/$NGINX_SITE
sudo ln -sf /etc/nginx/sites-available/$NGINX_SITE /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# # Setup SSL with Certbot
# echo "🔒 Setting up SSL certificate..."
# sudo certbot --nginx -d api.iitmquizzes.tech --non-interactive --agree-tos --email your-email@example.com

# # Setup firewall
# echo "🛡️ Configuring firewall..."
# sudo ufw allow ssh
# sudo ufw allow 'Nginx Full'
# sudo ufw --force enable

# Run database migrations
echo "🗄️ Running database setup..."
cd $APP_DIR
sudo -u www-data .venv/bin/python seed_data.py

echo "✅ Deployment completed successfully!"
echo "🌐 Your API should be available at: https://api.iitmquizzes.tech"
echo "🔍 Check service status: sudo systemctl status $SERVICE_NAME"
echo "📋 Check logs: sudo journalctl -u $SERVICE_NAME -f"
