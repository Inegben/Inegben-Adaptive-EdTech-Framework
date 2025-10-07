"""
Netlify-specific configuration for the IAEF backend
"""

import os
from typing import List

class NetlifySettings:
    """Netlify-specific settings for the application"""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./iaef_demo.db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - Netlify specific origins
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://*.netlify.app",  # Allow Netlify deployments
        "https://*.netlify.com",  # Allow Netlify previews
    ]
    
    # Add custom domain if provided
    if os.getenv("NETLIFY_SITE_URL"):
        ALLOWED_ORIGINS.append(os.getenv("NETLIFY_SITE_URL"))
    
    # Content
    CONTENT_BASE_URL: str = os.getenv("CONTENT_BASE_URL", "https://your-site.netlify.app/static/content")
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # Assessment
    ASSESSMENT_QUESTIONS_COUNT: int = 10
    LEARNING_STYLES: List[str] = ["visual", "auditory", "kinesthetic"]

# Create settings instance
netlify_settings = NetlifySettings()
