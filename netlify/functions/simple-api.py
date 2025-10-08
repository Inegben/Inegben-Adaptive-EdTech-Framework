"""
Simplified Netlify Function for API endpoints
"""

import json

def handler(event, context):
    """Main handler for all API requests"""
    
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
        method = event.get('httpMethod', '')
        path = event.get('path', '')
        
        print(f"Request: {method} {path}")
        
        # Simple test endpoint
        if path == '/api/v1/test' and method == 'GET':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'API is working!', 'path': path, 'method': method})
            }
        
        # Login endpoint
        if path == '/api/v1/users/login' and method == 'POST':
            query_params = event.get('queryStringParameters') or {}
            email = query_params.get('email')
            password = query_params.get('password')
            
            print(f"Login attempt: {email}")
            
            if email == 'alex@example.com' and password == 'password123':
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'access_token': 'demo_token_123',
                        'token_type': 'bearer',
                        'user': {
                            'id': 1,
                            'email': 'alex@example.com',
                            'username': 'alex_student',
                            'learning_style': 'visual',
                            'assessment_completed': True
                        }
                    })
                }
            else:
                return {
                    'statusCode': 401,
                    'headers': headers,
                    'body': json.dumps({'detail': 'Invalid credentials'})
                }
        
        # Register endpoint
        if path == '/api/v1/users/register' and method == 'POST':
            body = json.loads(event.get('body', '{}'))
            email = body.get('email')
            username = body.get('username')
            password = body.get('password')
            
            print(f"Registration attempt: {email}")
            
            if email and username and password:
                return {
                    'statusCode': 201,
                    'headers': headers,
                    'body': json.dumps({
                        'access_token': 'demo_token_456',
                        'token_type': 'bearer',
                        'user': {
                            'id': 999,
                            'email': email,
                            'username': username,
                            'learning_style': None,
                            'assessment_completed': False
                        }
                    })
                }
            else:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'detail': 'Email, username, and password are required'})
                }
        
        # Default response
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'detail': f'Endpoint not found: {method} {path}'})
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'detail': f'Internal server error: {str(e)}'})
        }
