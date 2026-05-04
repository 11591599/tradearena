#!/bin/bash
set -e

echo "🏆 TradeArena Deployment"
echo "========================"

# Update system
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx certbot python3-certbot-nginx

# Clone repo
cd /opt
if [ -d "tradearena" ]; then
    cd tradearena && git pull
else
    git clone https://github.com/11591599/tradearena.git
    cd tradearena
fi

# Setup environment
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Edit .env with your values:"
    echo "   nano /opt/tradearena/.env"
    exit 1
fi

# Backend setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend build
cd frontend
npm install
npm run build
cd ..

# Nginx config
sudo cp deploy/tradearena.conf /etc/nginx/sites-available/tradearena
sudo ln -sf /etc/nginx/sites-available/tradearena /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# SSL (uncomment when domain is ready)
# sudo certbot --nginx -d tradearena.app

echo "✅ Deployment complete!"
echo "Run: cd /opt/tradearena && source venv/bin/activate && python src/main.py"