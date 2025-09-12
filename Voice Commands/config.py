"""
Configuration settings for the API
"""

import os
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    app_name: str = "ManVue Enhanced API"
    app_version: str = "2.0.0"
    app_description: str = "Full-featured backend for MANVUE with MongoDB and ML integration"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 5001
    reload: bool = True
    
    # Database Configuration
    mongo_uri: str = "mongodb://localhost:27017"
    db_name: str = "manvue_db"
    
    # Security Configuration
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    # CORS Configuration
    allowed_origins: list = ["*"]  # In production, specify exact origins
    allowed_methods: list = ["*"]
    allowed_headers: list = ["*"]
    
    # File Upload Configuration
    max_file_size: int = 16 * 1024 * 1024  # 16MB
    allowed_image_types: list = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    
    # ML Configuration
    ml_enabled: bool = True
    ml_api_url: str = "http://localhost:5000"
    
    # API Configuration
    api_base_url: str = "http://localhost:5001"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    
    # Logging Configuration
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development environment settings"""
    debug: bool = True
    reload: bool = True
    log_level: str = "DEBUG"

class ProductionSettings(Settings):
    """Production environment settings"""
    debug: bool = False
    reload: bool = False
    log_level: str = "WARNING"
    allowed_origins: list = ["https://yourdomain.com"]  # Specify exact origins

class TestingSettings(Settings):
    """Testing environment settings"""
    debug: bool = True
    db_name: str = "manvue_test_db"
    mongo_uri: str = "mongodb://localhost:27017"

def get_environment_settings() -> Settings:
    """Get settings based on environment"""
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()
