from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Learning profile
    learning_style = Column(String, default=None)  # visual, auditory, kinesthetic
    assessment_completed = Column(Boolean, default=False)
    assessment_score = Column(JSON, default=None)  # {"visual": 3, "auditory": 2, "kinesthetic": 5}
    
    # Relationships
    progress_records = relationship("ProgressRecord", back_populates="user")
    content_interactions = relationship("ContentInteraction", back_populates="user")

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    visual_answer = Column(String, nullable=False)
    auditory_answer = Column(String, nullable=False)
    kinesthetic_answer = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Content(Base):
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    content_type = Column(String, nullable=False)  # video, audio, text, interactive
    subject = Column(String, nullable=False)
    difficulty_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    duration_minutes = Column(Integer, default=0)
    
    # Content URLs for different formats
    video_url = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)
    text_content = Column(Text, nullable=True)
    interactive_url = Column(String, nullable=True)
    
    # Metadata
    tags = Column(JSON, default=list)
    learning_objectives = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    progress_records = relationship("ProgressRecord", back_populates="content")
    content_interactions = relationship("ContentInteraction", back_populates="content")

class ProgressRecord(Base):
    __tablename__ = "progress_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    
    # Progress tracking
    completion_percentage = Column(Float, default=0.0)
    time_spent_minutes = Column(Integer, default=0)
    last_position = Column(Integer, default=0)  # For video/audio content
    is_completed = Column(Boolean, default=False)
    
    # Performance metrics
    quiz_score = Column(Float, nullable=True)
    engagement_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="progress_records")
    content = relationship("Content", back_populates="progress_records")

class ContentInteraction(Base):
    __tablename__ = "content_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    
    # Interaction details
    interaction_type = Column(String, nullable=False)  # view, play, pause, seek, format_switch
    format_used = Column(String, nullable=False)  # video, audio, text, interactive
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    duration_seconds = Column(Integer, default=0)
    interaction_metadata = Column(JSON, default=dict)  # Additional interaction data
    
    # Relationships
    user = relationship("User", back_populates="content_interactions")
    content = relationship("Content", back_populates="content_interactions")
