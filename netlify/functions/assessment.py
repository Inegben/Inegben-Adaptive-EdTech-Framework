"""
Netlify Function for assessment endpoints
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

# Sample assessment questions
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
    },
    {
        "id": 3,
        "question_text": "When studying, I like to:",
        "visual_answer": "Use highlighters, mind maps, and visual notes",
        "auditory_answer": "Read aloud or discuss with others",
        "kinesthetic_answer": "Take breaks and move around"
    },
    {
        "id": 4,
        "question_text": "I learn best from:",
        "visual_answer": "Pictures, videos, and demonstrations",
        "auditory_answer": "Lectures, podcasts, and group discussions",
        "kinesthetic_answer": "Experiments, building, and hands-on activities"
    },
    {
        "id": 5,
        "question_text": "When I need to understand something complex:",
        "visual_answer": "I draw diagrams or create visual representations",
        "auditory_answer": "I talk through it or explain it to someone",
        "kinesthetic_answer": "I try to build or create a model of it"
    }
]

def handler(event, context):
    """Handle assessment requests"""
    
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
        if path == '/api/v1/assessment/questions' and method == 'GET':
            return handle_questions(event, headers)
        elif path == '/api/v1/assessment/submit' and method == 'POST':
            return handle_submit(event, headers)
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

def handle_questions(event, headers):
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

def handle_submit(event, headers):
    """Handle assessment submission"""
    try:
        # Parse request body
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
        
        # Determine learning style (highest count)
        learning_style = max(style_counts, key=style_counts.get)
        
        # Return result
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
