"""
Netlify Function for content and dashboard endpoints
"""

import json
import os
import sys

# Set CORS headers
def get_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Content-Type': 'application/json'
    }

# Sample content data
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
    },
    {
        "id": 3,
        "title": "Data Science with Python",
        "description": "Analyze data and create visualizations using Python",
        "subject": "Data Science",
        "difficulty_level": "Intermediate",
        "duration_minutes": 90,
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "audio_url": None,
        "text_content": "Data science combines statistics, programming, and domain expertise to extract insights from data...",
        "interactive_url": None,
        "learning_objectives": [
            "Learn pandas for data manipulation",
            "Create visualizations with matplotlib",
            "Perform statistical analysis"
        ]
    }
]

def handler(event, context):
    """Handle content and dashboard requests"""
    
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
        
        # Route to appropriate handler
        if path == '/api/v1/content/recommendations/personalized' and method == 'GET':
            return handle_recommendations(event, headers)
        elif path == '/api/v1/analytics/dashboard/overview' and method == 'GET':
            return handle_dashboard_overview(event, headers)
        elif path.startswith('/api/v1/content/') and method == 'GET':
            return handle_content_detail(event, headers)
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

def handle_recommendations(event, headers):
    """Handle personalized content recommendations"""
    try:
        # Get query parameters
        query_params = event.get('queryStringParameters') or {}
        limit = int(query_params.get('limit', 6))
        
        # Return sample content (in production, this would be personalized)
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
        # Return sample dashboard data
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

def handle_content_detail(event, headers):
    """Handle individual content requests"""
    try:
        # Extract content ID from path
        path = event.get('path', '')
        content_id = int(path.split('/')[-1])
        
        # Find content by ID
        content = None
        for item in SAMPLE_CONTENT:
            if item['id'] == content_id:
                content = item
                break
        
        if not content:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'detail': 'Content not found'})
            }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(content)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'detail': f'Failed to get content: {str(e)}'})
        }
