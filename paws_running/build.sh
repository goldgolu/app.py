#!/bin/bash

echo "Starting Deployment Process..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=10000  # Render default port

# Ensure static files are correctly found
echo "Checking Static Files..."
if [ -d "static" ]; then
    echo "Static directory exists."
    find static -type d -exec chmod 755 {} \;
    find static -type f -exec chmod 644 {} \;
else
    echo "Static directory missing! Creating..."
    mkdir static
fi

# Ensure all subfolders exist
for dir in static/css static/js static/images static/fonts; do
    if [ ! -d "$dir" ]; then
        echo "Creating missing directory: $dir"
        mkdir -p "$dir"
    fi
done

echo "Static Files Checked and Fixed."

# Run Database Migrations (if required)
# flask db upgrade

# Start Flask App
echo "Starting Flask Application..."
gunicorn -w 4 -b 0.0.0.0:10000 app:app
