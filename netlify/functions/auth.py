"""
Netlify Function for authentication endpoints
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Optional
import hashlib

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

# Simple in-memory user storage for demo purposes
# In production, this would be a proper database
USERS = {
    "alex@example.com": {
        "id": 1,
        "email": "alex@example.com",
        "username": "alex_student",
        "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
        "learning_style": "visual",
        "assessment_completed": True,
        "created_at": datetime.now().isoformat()
    },
    "sarah@example.com": {
        "id": 2,
        "email": "sarah@example.com", 
        "username": "sarah_professional",
        "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
        "learning_style": "auditory",
        "assessment_completed": True,
        "created_at": datetime.now().isoformat()
    },
    "mike@example.com": {
        "id": 3,
        "email": "mike@example.com",
        "username": "mike_learner", 
        "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
        "learning_style": "kinesthetic",
        "assessment_completed": True,
        "created_at": datetime.now().isoformat()
    }
}

def generate_token(user_id: int) -> str:
    """Generate a simple token for demo purposes"""
    import time
    return f"demo_token_{user_id}_{int(time.time())}"

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return hashlib.sha256(password.encode()).hexdigest() == password_hash

def handler(event, context):
    """Handle authentication requests"""
    
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        # Parse the request
        method = event.get('httpMethod', '')
        path = event.get('path', '')
        
        # Route to appropriate handler
        if path == '/api/v1/users/login' and method == 'POST':
            return handle_login(event, headers)
        elif path == '/api/v1/users/register' and method == 'POST':
            return handle_register(event, headers)
        elif path == '/api/v1/users/me' and method == 'GET':
            return handle_me(event, headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'detail': 'Not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'detail': f'Internal server error: {str(e)}'})
        }

def handle_login(event, headers):
    """Handle user login"""
    try:
        # Parse query parameters
        query_params = event.get('queryStringParameters') or {}
        email = query_params.get('email')
        password = query_params.get('password')
        
        if not email or not password:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'detail': 'Email and password are required'})
            }
        
        # Check if user exists
        if email not in USERS:
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'detail': 'Invalid credentials'})
            }
        
        user = USERS[email]
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'detail': 'Invalid credentials'})
            }
        
        # Generate token
        token = generate_token(user['id'])
        
        # Return user data and token
        user_data = {
            'id': user['id'],
            'email': user['email'],
            'username': user['username'],
            'learning_style': user['learning_style'],
            'assessment_completed': user['assessment_completed']
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'access_token': token,
                'token_type': 'bearer',
                'user': user_data
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'detail': f'Login failed: {str(e)}'})
        }

def handle_register(event, headers):
    """Handle user registration"""
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        username = body.get('username')
        password = body.get('password')
        
        if not email or not username or not password:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'detail': 'Email, username, and password are required'})
            }
        
        # Check if user already exists
        if email in USERS:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'detail': 'User already exists'})
            }
        
        # Create new user
        user_id = max([u['id'] for u in USERS.values()]) + 1 if USERS else 1
        USERS[email] = {
            'id': user_id,
            'email': email,
            'username': username,
            'password_hash': hashlib.sha256(password.encode()).hexdigest(),
            'learning_style': None,
            'assessment_completed': False,
            'created_at': datetime.now().isoformat()
        }
        
        # Auto-login after registration
        token = generate_token(user_id)
        user_data = {
            'id': user_id,
            'email': email,
            'username': username,
            'learning_style': None,
            'assessment_completed': False
        }
        
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps({
                'access_token': token,
                'token_type': 'bearer',
                'user': user_data
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'detail': f'Registration failed: {str(e)}'})
        }

def handle_me(event, headers):
    """Handle get current user"""
    try:
        # Get authorization header
        auth_header = event.get('headers', {}).get('authorization', '')
        if not auth_header.startswith('Bearer '):
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'detail': 'Invalid token'})
            }
        
        token = auth_header.split(' ')[1]
        
        # Simple token validation (in production, use proper JWT)
        if not token.startswith('demo_token_'):
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'detail': 'Invalid token'})
            }
        
        # Extract user ID from token
        try:
            user_id = int(token.split('_')[2])
        except:
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'detail': 'Invalid token'})
            }
        
        # Find user by ID
        user = None
        for email, user_data in USERS.items():
            if user_data['id'] == user_id:
                user = user_data
                break
        
        if not user:
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'detail': 'User not found'})
            }
        
        # Return user data
        user_data = {
            'id': user['id'],
            'email': user['email'],
            'username': user['username'],
            'learning_style': user['learning_style'],
            'assessment_completed': user['assessment_completed']
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(user_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'detail': f'Failed to get user: {str(e)}'})
        }
