"""
Netlify Functions wrapper for FastAPI backend
This file adapts the FastAPI app for Netlify Functions
"""

import json
import asyncio
from mangum import Mangum
from backend.app.main import app

# Create Mangum adapter for Netlify Functions
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    """
    Netlify Functions entry point
    """
    # Handle CORS preflight requests
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
            },
            'body': ''
        }
    
    # Process the request through Mangum
    response = handler(event, context)
    
    # Ensure response is properly formatted
    if asyncio.iscoroutine(response):
        response = asyncio.run(response)
    
    return response
