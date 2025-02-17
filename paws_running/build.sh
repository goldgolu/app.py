#!/bin/bash

echo "Starting Deployment Process..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt || { echo "❌ Failed to install dependencies"; exit 1; }

# Set environment variables
export FLASK_APP=paws_running/app.py  # Correct path
export FLASK_ENV=production
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=10000  # Render's default port

# Ensure static and templates directories exist
echo "Checking Static & Template Files..."
if [ ! -d "paws_running/static" ]; then
    echo "Static directory missing! Creating..."
    mkdir -p paws_running/static
fi

if [ ! -d "paws_running/templates" ]; then
    echo "Templates directory missing! Creating..."
    mkdir -p paws_running/templates
fi

# Apply correct permissions
echo "Fixing permissions for static and template files..."
find paws_running/static -type d -exec chmod 755 {} \;
find paws_running/static -type f -exec chmod 644 {} \;
find paws_running/templates -type d -exec chmod 755 {} \;
find paws_running/templates -type f -exec chmod 644 {} \;

echo "Static & Template Files Checked and Fixed."

# Start Flask App with Gunicorn
echo "Starting Flask Application..."
cd paws_running  # Go inside project folder
gunicorn -w 4 -b 0.0.0.0:10000 app:app
