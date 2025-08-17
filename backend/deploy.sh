#!/bin/bash
# CoinCraft Backend Deployment Script

set -e

echo "🚀 Starting CoinCraft Backend Deployment..."

# Check if we're in the backend directory
if [ ! -f "main.py" ] || [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the backend directory of your cloned repository"
    echo "Current directory: $(pwd)"
    echo "Expected files: main.py, pyproject.toml"
    exit 1
fi

echo "✅ Running from backend directory: $(pwd)"

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

# Copy repository files (assuming you've already cloned the repo)
echo "📥 Copying repository files..."
echo "Note: Running from $(pwd)"
sudo cp -r ./* $APP_DIR/
sudo cp -r ./.env* $APP_DIR/ 2>/dev/null || true  # Copy .env files if they exist

# Set permissions
echo "🔐 Setting permissions..."
sudo chown -R www-data:www-data $APP_DIR
sudo chown -R www-data:www-data /var/log/coincraft

# Setup Python environment
echo "🐍 Setting up Python environment..."
cd $APP_DIR
sudo -u www-data uv venv
sudo -u www-data uv pip install -r requirements.txt

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

# Setup firewall
# echo "🛡️ Configuring firewall..."
# sudo ufw allow ssh
# sudo ufw allow 'Nginx Full'
# sudo ufw --force enable

# Run database migrations
echo "🗄️ Running database setup..."
cd $APP_DIR
sudo -u www-data .venv/bin/uv run seed_data.py

echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Your API should be available at: https://api.iitmquizzes.tech"
echo "🔍 Check service status: sudo systemctl status $SERVICE_NAME"
echo "📋 Check logs: sudo journalctl -u $SERVICE_NAME -f"
echo "🔄 Restart service: sudo systemctl restart $SERVICE_NAME"
echo "🔧 Reload nginx: sudo systemctl reload nginx"
echo ""
echo "📝 Next steps:"
echo "1. Update DNS to point api.iitmquizzes.tech to this server's IP"
echo "2. Test the API: curl https://api.iitmquizzes.tech/health"
echo "3. Update frontend CORS origins with your Vercel URL"
