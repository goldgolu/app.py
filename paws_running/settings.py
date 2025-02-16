import os  # Importing os module

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, '../static')
TEMPLATE_FOLDER = os.path.join(BASE_DIR, '../templates')

# Print paths for debugging
print(f"TEMPLATE_FOLDER: {TEMPLATE_FOLDER}")
print(f"STATIC_FOLDER: {STATIC_FOLDER}")

# Render Deployment Config
DEBUG = False
PORT = 5000  # Syncing with FLASK_SERVER_URL
HOST = "0.0.0.0"

# Database Config (Future use case)
# DB_URI = "mysql://user:password@host/dbname"  # Example
