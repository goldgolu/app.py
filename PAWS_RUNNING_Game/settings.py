import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Static aur Templates ka path define karo
STATIC_FOLDER = os.path.join(BASE_DIR, "static")
TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")

# Flask Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Database Configuration
DB_NAME = "game_data.db"
DB_PATH = os.path.join(os.getcwd(), DB_NAME)
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# WhiteNoise Configuration (if using for serving static files)
USE_WHITENOISE = os.getenv("USE_WHITENOISE", "False").lower() == "true"

# Telegram Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_default_bot_token")
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))  # Replace with actual owner ID

# Instagram API Configuration
INSTAGRAM_CLIENT_ID = os.getenv("INSTAGRAM_CLIENT_ID", "your_client_id")
INSTAGRAM_CLIENT_SECRET = os.getenv("INSTAGRAM_CLIENT_SECRET", "your_client_secret")

# Game Settings
MAX_PLAYERS = int(os.getenv("MAX_PLAYERS", "100"))
ENABLE_AI_BOT = os.getenv("ENABLE_AI_BOT", "True").lower() == "true"

# Socket.IO Configuration (if using Flask-SocketIO)
USE_SOCKETIO = os.getenv("USE_SOCKETIO", "False").lower() == "true"
SOCKETIO_CORS_ALLOWED_ORIGINS = "*"
