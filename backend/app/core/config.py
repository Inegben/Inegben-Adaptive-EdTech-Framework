from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./iaef_demo.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://*.vercel.app",  # Allow Vercel deployments
        "https://iaef-frontend.vercel.app"  # Your frontend domain
    ]
    
    # Content
    CONTENT_BASE_URL: str = "http://localhost:8000/static/content"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # Assessment
    ASSESSMENT_QUESTIONS_COUNT: int = 10
    LEARNING_STYLES: List[str] = ["visual", "auditory", "kinesthetic"]
    
    class Config:
        env_file = ".env"

settings = Settings()
