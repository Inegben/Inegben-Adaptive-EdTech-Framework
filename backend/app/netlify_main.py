"""
Netlify-optimized FastAPI application
This version is specifically configured for Netlify Functions deployment
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import os

from app.database import get_db, engine
from app.models import Base
from app.routers import users, assessment, content, analytics
from backend.netlify_config import netlify_settings

# Create database tables (only if not in serverless environment)
if not os.getenv("NETLIFY"):
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IAEF - Inegben Adaptive EdTech Framework (Netlify)",
    description="A comprehensive educational technology framework for adaptive learning experiences - Netlify Functions version",
    version="1.0.0"
)

# CORS middleware with Netlify-specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=netlify_settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(assessment.router, prefix="/api/v1/assessment", tags=["assessment"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to IAEF - Inegben Adaptive EdTech Framework (Netlify)",
        "version": "1.0.0",
        "status": "active",
        "platform": "netlify"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "IAEF Backend (Netlify)"}

# Netlify Functions specific endpoints
@app.get("/.netlify/functions/api")
async def netlify_function_info():
    return {
        "message": "IAEF API running on Netlify Functions",
        "endpoints": {
            "users": "/api/v1/users",
            "assessment": "/api/v1/assessment", 
            "content": "/api/v1/content",
            "analytics": "/api/v1/analytics"
        }
    }
