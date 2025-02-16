import os  

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # Ye ensure karega ki templates sahi path pe mile
STATIC_FOLDER = os.path.join(PROJECT_ROOT, 'static')
TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, 'templates')

# Render Deployment Config
DEBUG = False
PORT = int(os.getenv("PORT", 5000))  # Render ka PORT variable use karega
HOST = "0.0.0.0"
