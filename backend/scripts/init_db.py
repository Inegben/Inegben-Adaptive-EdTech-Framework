#!/usr/bin/env python3
"""
Database initialization script for IAEF
Creates tables and populates with sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import sessionmaker
from app.database import engine, Base
from app.models import User, AssessmentQuestion, Content
from app.core.config import settings
from passlib.context import CryptContext

# Create tables
Base.metadata.create_all(bind=engine)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_sample_users():
    """Create sample users for testing"""
    print("Creating sample users...")
    
    # Check if users already exist
    if db.query(User).first():
        print("Users already exist, skipping...")
        return
    
    users = [
        {
            "email": "alex@example.com",
            "username": "alex_student",
            "password": "password123",
            "learning_style": "visual",
            "assessment_completed": True,
            "assessment_score": {"visual": 7, "auditory": 2, "kinesthetic": 1}
        },
        {
            "email": "sarah@example.com", 
            "username": "sarah_professional",
            "password": "password123",
            "learning_style": "auditory",
            "assessment_completed": True,
            "assessment_score": {"visual": 2, "auditory": 7, "kinesthetic": 1}
        },
        {
            "email": "mike@example.com",
            "username": "mike_learner", 
            "password": "password123",
            "learning_style": "kinesthetic",
            "assessment_completed": True,
            "assessment_score": {"visual": 1, "auditory": 2, "kinesthetic": 7}
        }
    ]
    
    for user_data in users:
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            hashed_password=hash_password(user_data["password"]),
            learning_style=user_data["learning_style"],
            assessment_completed=user_data["assessment_completed"],
            assessment_score=user_data["assessment_score"]
        )
        db.add(user)
    
    db.commit()
    print(f"Created {len(users)} sample users")

def create_sample_content():
    """Create sample educational content"""
    print("Creating sample content...")
    
    # Check if content already exists
    if db.query(Content).first():
        print("Content already exists, skipping...")
        return
    
    content_items = [
        {
            "title": "Introduction to Python Programming",
            "description": "Learn the basics of Python programming language with hands-on examples and interactive exercises.",
            "content_type": "video",
            "subject": "Programming",
            "difficulty_level": "beginner",
            "duration_minutes": 45,
            "video_url": "https://www.youtube.com/watch?v=kqtD5dpn9C8",
            "audio_url": "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav",
            "text_content": "Python is a high-level, interpreted programming language known for its simplicity and readability. In this lesson, we'll cover:\n\n1. Variables and Data Types\n2. Control Structures (if/else, loops)\n3. Functions\n4. Basic Data Structures (lists, dictionaries)\n\nPython uses indentation to define code blocks, making it very readable. Let's start with variables...",
            "interactive_url": "https://replit.com/@python-basics",
            "tags": ["python", "programming", "beginner", "coding"],
            "learning_objectives": [
                "Understand Python syntax and basic concepts",
                "Write simple Python programs",
                "Use variables and data types effectively",
                "Implement control structures"
            ]
        },
        {
            "title": "Machine Learning Fundamentals",
            "description": "Explore the core concepts of machine learning including supervised and unsupervised learning algorithms.",
            "content_type": "video",
            "subject": "Data Science",
            "difficulty_level": "intermediate",
            "duration_minutes": 60,
            "video_url": "https://www.youtube.com/watch?v=ukzFI9rgwfU",
            "audio_url": "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav",
            "text_content": "Machine Learning is a subset of artificial intelligence that focuses on algorithms that can learn from data. Key concepts include:\n\n1. Supervised Learning (Classification, Regression)\n2. Unsupervised Learning (Clustering, Dimensionality Reduction)\n3. Model Evaluation and Validation\n4. Feature Engineering\n\nWe'll explore each of these concepts with practical examples...",
            "interactive_url": "https://colab.research.google.com/",
            "tags": ["machine-learning", "ai", "data-science", "algorithms"],
            "learning_objectives": [
                "Understand different types of machine learning",
                "Implement basic ML algorithms",
                "Evaluate model performance",
                "Apply feature engineering techniques"
            ]
        },
        {
            "title": "Web Development with React",
            "description": "Build modern web applications using React.js with hooks, state management, and component architecture.",
            "content_type": "video",
            "subject": "Web Development",
            "difficulty_level": "intermediate",
            "duration_minutes": 90,
            "video_url": "https://www.youtube.com/watch?v=DLX62G4lc44",
            "audio_url": "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav",
            "text_content": "React is a JavaScript library for building user interfaces, particularly web applications. Key concepts include:\n\n1. Components and JSX\n2. State and Props\n3. Hooks (useState, useEffect)\n4. Event Handling\n5. Component Lifecycle\n\nReact uses a virtual DOM for efficient updates and provides a component-based architecture...",
            "interactive_url": "https://codesandbox.io/",
            "tags": ["react", "javascript", "web-development", "frontend"],
            "learning_objectives": [
                "Build React components",
                "Manage component state",
                "Use React hooks effectively",
                "Create interactive user interfaces"
            ]
        },
        {
            "title": "Database Design Principles",
            "description": "Learn fundamental database design concepts including normalization, relationships, and query optimization.",
            "content_type": "text",
            "subject": "Database",
            "difficulty_level": "beginner",
            "duration_minutes": 30,
            "video_url": "https://www.youtube.com/watch?v=ztHopE5Wnpc",
            "audio_url": "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav",
            "text_content": "Database design is crucial for creating efficient and maintainable data storage systems. Key principles include:\n\n1. Normalization (1NF, 2NF, 3NF)\n2. Entity-Relationship Modeling\n3. Primary and Foreign Keys\n4. Indexing and Performance\n5. Data Integrity Constraints\n\nGood database design reduces redundancy, improves performance, and ensures data consistency...",
            "interactive_url": "https://dbdiagram.io/",
            "tags": ["database", "sql", "design", "normalization"],
            "learning_objectives": [
                "Design normalized database schemas",
                "Create entity-relationship diagrams",
                "Implement proper indexing strategies",
                "Ensure data integrity"
            ]
        },
        {
            "title": "Cybersecurity Fundamentals",
            "description": "Understand the basics of cybersecurity including threats, vulnerabilities, and protection strategies.",
            "content_type": "interactive",
            "subject": "Security",
            "difficulty_level": "beginner",
            "duration_minutes": 40,
            "video_url": "https://www.youtube.com/watch?v=inWWhr5tnEA",
            "audio_url": "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav",
            "text_content": "Cybersecurity involves protecting digital systems, networks, and data from cyber threats. Key areas include:\n\n1. Threat Landscape (Malware, Phishing, Ransomware)\n2. Security Controls (Firewalls, Antivirus, Encryption)\n3. Risk Assessment and Management\n4. Incident Response\n5. Security Awareness and Training\n\nUnderstanding these concepts helps protect against evolving cyber threats...",
            "interactive_url": "https://tryhackme.com/",
            "tags": ["cybersecurity", "security", "threats", "protection"],
            "learning_objectives": [
                "Identify common cyber threats",
                "Implement security controls",
                "Conduct risk assessments",
                "Develop incident response plans"
            ]
        }
    ]
    
    for content_data in content_items:
        content = Content(**content_data)
        db.add(content)
    
    db.commit()
    print(f"Created {len(content_items)} sample content items")

def main():
    """Main initialization function"""
    print("Initializing IAEF Database...")
    print(f"Database URL: {settings.DATABASE_URL}")
    
    try:
        create_sample_users()
        create_sample_content()
        print("\n✅ Database initialization completed successfully!")
        print("\nSample users created:")
        print("- alex@example.com / alex_student (Visual Learner)")
        print("- sarah@example.com / sarah_professional (Auditory Learner)")
        print("- mike@example.com / mike_learner (Kinesthetic Learner)")
        print("\nPassword for all users: password123")
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
