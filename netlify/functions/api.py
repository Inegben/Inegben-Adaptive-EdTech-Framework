"""
Unified Netlify Function for all API endpoints
"""

import json
import hashlib
import time
from datetime import datetime

# Set CORS headers
def get_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Content-Type': 'application/json'
    }

# Sample users
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

# Sample content
SAMPLE_CONTENT = [
    {
        "id": 1,
        "title": "Introduction to Machine Learning",
        "description": "Learn the fundamentals of machine learning and artificial intelligence",
        "subject": "Computer Science",
        "difficulty_level": "Beginner",
        "duration_minutes": 45,
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "audio_url": None,
        "text_content": "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data...",
        "interactive_url": None,
        "learning_objectives": [
            "Understand basic ML concepts",
            "Learn about different types of learning",
            "Explore real-world applications"
        ]
    },
    {
        "id": 2,
        "title": "Web Development Fundamentals",
        "description": "Master the basics of HTML, CSS, and JavaScript",
        "subject": "Web Development",
        "difficulty_level": "Beginner",
        "duration_minutes": 60,
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "audio_url": None,
        "text_content": "Web development involves creating websites and web applications using various technologies...",
        "interactive_url": None,
        "learning_objectives": [
            "Learn HTML structure",
            "Style with CSS",
            "Add interactivity with JavaScript"
        ]
    }
]

# Assessment questions
ASSESSMENT_QUESTIONS = [
    {
        "id": 1,
        "question_text": "When learning something new, I prefer to:",
        "visual_answer": "See diagrams, charts, and visual representations",
        "auditory_answer": "Listen to explanations and discussions",
        "kinesthetic_answer": "Try it out hands-on and practice"
    },
    {
        "id": 2,
        "question_text": "I remember information best when I:",
        "visual_answer": "Write it down or see it written",
        "auditory_answer": "Hear it spoken or discuss it",
        "kinesthetic_answer": "Do something with it or experience it"
    }
]

def generate_token(user_id):
    """Generate a simple token for demo purposes"""
    return f"demo_token_{user_id}_{int(time.time())}"

def verify_password(password, password_hash):
    """Verify password against hash"""
    return hashlib.sha256(password.encode()).hexdigest() == password_hash

def handler(event, context):
    """Main handler for all API requests"""
    
    headers = get_headers()
    
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
        
        print(f"Request: {method} {path}")  # Debug logging
        
        # Route requests
        if path == '/api/v1/users/login' and method == 'POST':
            return handle_login(event, headers)
        elif path == '/api/v1/users/register' and method == 'POST':
            return handle_register(event, headers)
        elif path == '/api/v1/users/me' and method == 'GET':
            return handle_me(event, headers)
        elif path == '/api/v1/assessment/questions' and method == 'GET':
            return handle_assessment_questions(event, headers)
        elif path == '/api/v1/assessment/submit' and method == 'POST':
            return handle_assessment_submit(event, headers)
        elif path == '/api/v1/content/recommendations/personalized' and method == 'GET':
            return handle_recommendations(event, headers)
        elif path == '/api/v1/analytics/dashboard/overview' and method == 'GET':
            return handle_dashboard_overview(event, headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'detail': f'Endpoint not found: {method} {path}'})
            }
            
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug logging
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
        
        print(f"Login attempt: {email}")  # Debug logging
        
        if not email or not password:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'detail': 'Email and password are required'})
            }
        
        # Check if user exists
        if email not in USERS:
            print(f"User not found: {email}")  # Debug logging
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'detail': 'Invalid credentials'})
            }
        
        user = USERS[email]
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            print(f"Invalid password for: {email}")  # Debug logging
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
        
        print(f"Login successful for: {email}")  # Debug logging
        
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
        print(f"Login error: {str(e)}")  # Debug logging
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
        
        print(f"Registration attempt: {email}")  # Debug logging
        
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
        
        print(f"Registration successful for: {email}")  # Debug logging
        
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
        print(f"Registration error: {str(e)}")  # Debug logging
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
        
        # Simple token validation
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

def handle_assessment_questions(event, headers):
    """Handle getting assessment questions"""
    try:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(ASSESSMENT_QUESTIONS)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'detail': f'Failed to get questions: {str(e)}'})
        }

def handle_assessment_submit(event, headers):
    """Handle assessment submission"""
    try:
        body = json.loads(event.get('body', '{}'))
        answers = body.get('answers', [])
        
        if not answers:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'detail': 'Answers are required'})
            }
        
        # Count answers by learning style
        style_counts = {'visual': 0, 'auditory': 0, 'kinesthetic': 0}
        
        for answer in answers:
            style = answer.get('answer')
            if style in style_counts:
                style_counts[style] += 1
        
        # Determine learning style
        learning_style = max(style_counts, key=style_counts.get)
        
        result = {
            'learning_style': learning_style,
            'scores': style_counts,
            'message': f'Based on your answers, you are a {learning_style} learner!'
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'detail': f'Failed to submit assessment: {str(e)}'})
        }

def handle_recommendations(event, headers):
    """Handle personalized content recommendations"""
    try:
        query_params = event.get('queryStringParameters') or {}
        limit = int(query_params.get('limit', 6))
        
        recommendations = SAMPLE_CONTENT[:limit]
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(recommendations)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'detail': f'Failed to get recommendations: {str(e)}'})
        }

def handle_dashboard_overview(event, headers):
    """Handle dashboard overview data"""
    try:
        dashboard_data = {
            "total_time_minutes": 120,
            "content_completed": 2,
            "content_in_progress": 1,
            "assessment_completed": True,
            "format_usage": {
                "video": 5,
                "text": 3,
                "audio": 1,
                "interactive": 2
            }
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(dashboard_data)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'detail': f'Failed to get dashboard data: {str(e)}'})
        }