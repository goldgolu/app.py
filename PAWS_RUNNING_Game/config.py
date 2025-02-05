import os

class Config:
    """
    Flask application configuration.
    """
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
    DEBUG = os.getenv("DEBUG", "True") == "True"
    
    # Templates and Static files configuration
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")
    STATIC_FOLDER = os.path.join(BASE_DIR, "static")
    
    # Database Configuration (Modify as per your database choice)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///game.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Game settings
    MAX_PLAYERS = int(os.getenv("MAX_PLAYERS", 100))
    AIRDROP_FREQUENCY = int(os.getenv("AIRDROP_FREQUENCY", 5))  # in minutes
    
    # AI Robot Settings
    AI_ENABLED = os.getenv("AI_ENABLED", "True") == "True"
    AI_NAME = "Ai Robota"
    
    # Other settings
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Load the configuration
config = Config()
