# settings.py

STATIC_FOLDER = "static"
TEMPLATE_FOLDER = "templates"

# Render Deployment Config
DEBUG = False
PORT = 10000
HOST = "0.0.0.0"

# Database Config (Agar Future me Required ho)
# DB_URI = "mysql://user:password@host/dbname"  # Example

-----------------------------

# build.sh

#!/bin/bash

# Ensure script runs with error handling
echo "Starting Build Process..."
set -e

# Create static files directory if not exists
mkdir -p static
mkdir -p templates

# Fix permissions
chmod -R 755 static templates

# Run Flask App
flask run --host=$HOST --port=$PORT
