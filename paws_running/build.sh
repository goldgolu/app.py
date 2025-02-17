#!/bin/bash

echo "Starting Deployment Process..."

# Install dependencies with retry mechanism
echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
MAX_RETRIES=3
RETRY_COUNT=0
SUCCESS=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  pip install -r requirements.txt && SUCCESS=true && break
  echo "❌ Failed to install dependencies. Retrying... ($((RETRY_COUNT+1))/$MAX_RETRIES)"
  ((RETRY_COUNT++))
  sleep 5
done

if [ "$SUCCESS" != true ]; then
  echo "❌ Failed to install dependencies after $MAX_RETRIES attempts"
  exit 1
fi

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

# Ensure Gunicorn is installed and available
echo "Checking for Gunicorn..."
if ! command -v gunicorn &> /dev/null
then
    echo "❌ Gunicorn not found. Installing..."
    pip install gunicorn
else
    echo "✅ Gunicorn is already installed."
fi

# Start Flask App with Gunicorn
echo "Starting Flask Application..."
cd paws_running  # Go inside project folder
gunicorn -w 4 -b 0.0.0.0:10000 app:app
