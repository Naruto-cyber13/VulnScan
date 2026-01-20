"""
Configuration module for LogLens/VulnScan Lite. 
Loads environment variables and centralizes configuration. 
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

class Settings:
    """Application configuration settings."""
    
    # Project metadata
    PROJECT_NAME:  str = "VulnScan Lite"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Lightweight security analysis platform for on-demand scanning"
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./security_scans.db")
    SQLALCHEMY_ECHO: bool = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"
    
    # HTTP request configuration
    HTTP_TIMEOUT: int = int(os.getenv("HTTP_TIMEOUT", 10))
    HTTP_MAX_RETRIES: int = int(os.getenv("HTTP_MAX_RETRIES", 2))
    
    # Feature flags
    ENABLE_HISTORY: bool = os.getenv("ENABLE_HISTORY", "True").lower() == "true"
    
    # Logging configuration
    LOG_LEVEL:  str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: str = os.getenv("LOG_DIR", "app/logs")
    
    @classmethod
    def ensure_log_directory(cls):
        """Create log directory if it doesn't exist."""
        Path(cls.LOG_DIR).mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.ensure_log_directory()
print("📦 DATABASE_URL Loaded:", settings.DATABASE_URL)
