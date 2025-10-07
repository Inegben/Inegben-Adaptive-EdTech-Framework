from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    learning_style: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    learning_style: Optional[str] = None
    assessment_completed: bool
    assessment_score: Optional[Dict[str, int]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Assessment Schemas
class AssessmentAnswer(BaseModel):
    question_id: int
    answer: str  # "visual", "auditory", "kinesthetic"

class AssessmentSubmission(BaseModel):
    answers: List[AssessmentAnswer]

class AssessmentResult(BaseModel):
    learning_style: str
    scores: Dict[str, int]
    confidence: float

class AssessmentQuestion(BaseModel):
    id: int
    question_text: str
    visual_answer: str
    auditory_answer: str
    kinesthetic_answer: str

# Content Schemas
class ContentBase(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str
    difficulty_level: str = "beginner"
    duration_minutes: int = 0
    tags: List[str] = []
    learning_objectives: List[str] = []

class ContentCreate(ContentBase):
    content_type: str
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    text_content: Optional[str] = None
    interactive_url: Optional[str] = None

class Content(ContentBase):
    id: int
    content_type: str
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    text_content: Optional[str] = None
    interactive_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class AdaptiveContentResponse(BaseModel):
    content: Content
    recommended_format: str
    alternative_formats: List[str]
    personalization_reason: str

# Progress Schemas
class ProgressRecord(BaseModel):
    id: int
    user_id: int
    content_id: int
    completion_percentage: float
    time_spent_minutes: int
    last_position: int
    is_completed: bool
    quiz_score: Optional[float] = None
    engagement_score: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ProgressUpdate(BaseModel):
    completion_percentage: Optional[float] = None
    time_spent_minutes: Optional[int] = None
    last_position: Optional[int] = None
    is_completed: Optional[bool] = None
    quiz_score: Optional[float] = None

# Interaction Schemas
class ContentInteraction(BaseModel):
    interaction_type: str
    format_used: str
    duration_seconds: int = 0
    interaction_metadata: Dict[str, Any] = {}

class InteractionCreate(ContentInteraction):
    content_id: int

# Analytics Schemas
class UserAnalytics(BaseModel):
    user_id: int
    total_time_spent: int
    content_completed: int
    average_engagement: float
    preferred_format: str
    learning_style: str
    progress_trend: List[Dict[str, Any]]

class ContentAnalytics(BaseModel):
    content_id: int
    total_views: int
    completion_rate: float
    average_engagement: float
    format_preferences: Dict[str, int]
    user_feedback: Dict[str, Any]
