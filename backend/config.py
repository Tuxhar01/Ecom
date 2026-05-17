import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-change-in-production')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///bookstore.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS Configuration
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    
    # AIRA Configuration
    AIRA_WEBHOOK_URL = os.getenv('AIRA_WEBHOOK_URL')
    AIRA_API_KEY = os.getenv('AIRA_API_KEY')
    AIRA_ENABLED = os.getenv('AIRA_ENABLED', 'true').lower() == 'true'
    AIRA_LOG_LEVEL = os.getenv('AIRA_LOG_LEVEL', 'ERROR')
    AIRA_MAX_RETRIES = int(os.getenv('AIRA_MAX_RETRIES', 3))
    AIRA_TIMEOUT = int(os.getenv('AIRA_TIMEOUT', 5))
    AIRA_RATE_LIMIT = int(os.getenv('AIRA_RATE_LIMIT', 100))
    
    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours

# Made with Bob
