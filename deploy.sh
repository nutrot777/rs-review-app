#!/bin/bash

# RS Review Deployment Script for University Server
# Make sure Python 3.9+ and pip are installed

echo "🚀 Starting RS Review Application Deployment..."

# Create virtual environment
python3 -m venv rs_review_env
source rs_review_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make run script executable
chmod +x run_all.py

# Set up as systemd service (optional)
sudo cp rs-review.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rs-review
sudo systemctl start rs-review

echo "✅ Deployment complete!"
echo "🌐 Access your application at: http://your-server-ip:3000"