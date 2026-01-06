from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/ned_university_docs"
    
    # Application
    app_name: str = "NED University Document Management System"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Admin Authentication
    admin_username: str = "admin"
    admin_password: str = "ned@admin123"
    jwt_secret_key: str = "your-secret-key-change-this-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    
    # File Storage
    upload_dir: str = "./uploads"
    max_file_size: int = 10485760  # 10MB
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:3001"
    
    # Tesseract
    tesseract_cmd: str = "/usr/bin/tesseract"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
