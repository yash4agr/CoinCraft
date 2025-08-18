#!/bin/bash
# Quick fix for uv command not found issue

echo "🔧 Fixing uv command path issue..."

# Export PATH for current session
export PATH="/root/.local/bin:$PATH"

# Make uv available system-wide
echo "🔗 Creating system-wide symlinks for uv..."
sudo ln -sf /root/.local/bin/uv /usr/local/bin/uv
sudo ln -sf /root/.local/bin/uvx /usr/local/bin/uvx

# Verify uv is now accessible
echo "✅ Verifying uv installation..."
uv --version

echo "🐍 Setting up Python environment manually..."
cd /var/www/coincraft/backend

# Create virtual environment
uv venv .venv

# Install dependencies
uv pip install -r requirements.txt

# Fix permissions
sudo chown -R www-data:www-data .venv

# Setup database
echo "🗄️ Setting up database..."
sudo -u www-data .venv/bin/python seed_data.py

# Start the service
echo "🚀 Starting coincraft service..."
sudo systemctl daemon-reload
sudo systemctl enable coincraft
sudo systemctl start coincraft

echo "✅ Quick fix completed!"
echo "🔍 Check service status: sudo systemctl status coincraft"
