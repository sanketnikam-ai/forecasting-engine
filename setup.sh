#!/bin/bash
# Quick setup script for VPS deployment

echo "========================================="
echo "Forecasting Engine - VPS Setup Script"
echo "========================================="

# Update system
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx (optional)
read -p "Install Nginx? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Installing Nginx..."
    sudo apt install -y nginx
    sudo systemctl enable nginx
fi

# Clone repository
read -p "Enter your GitHub repository URL: " REPO_URL
git clone $REPO_URL forecasting-engine
cd forecasting-engine

# Build and start
echo "Building and starting application..."
docker-compose up -d

# Show status
echo ""
echo "========================================="
echo "Setup complete!"
echo "========================================="
echo "Application is running on port 5000"
echo ""
echo "To check status: docker-compose ps"
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
echo ""

# Get server IP
SERVER_IP=$(curl -s ifconfig.me)
echo "Access your app at: http://$SERVER_IP:5000"
echo ""

# Setup Nginx if installed
if command -v nginx &> /dev/null; then
    echo "To setup Nginx reverse proxy:"
    echo "1. Edit nginx.conf with your domain"
    echo "2. sudo cp nginx.conf /etc/nginx/sites-available/forecasting"
    echo "3. sudo ln -s /etc/nginx/sites-available/forecasting /etc/nginx/sites-enabled/"
    echo "4. sudo nginx -t && sudo systemctl reload nginx"
fi

echo ""
echo "For SSL certificate (Let's Encrypt):"
echo "sudo apt install certbot python3-certbot-nginx"
echo "sudo certbot --nginx -d your-domain.com"
