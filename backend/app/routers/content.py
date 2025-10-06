from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import User, Content, ProgressRecord, ContentInteraction
from app.schemas import Content as ContentSchema, AdaptiveContentResponse, ProgressUpdate, InteractionCreate
from app.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ContentSchema])
async def get_content_list(
    subject: Optional[str] = Query(None, description="Filter by subject"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty level"),
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    db: Session = Depends(get_db)
):
    """Get list of available content with optional filters."""
    query = db.query(Content).filter(Content.is_active == True)
    
    if subject:
        query = query.filter(Content.subject.ilike(f"%{subject}%"))
    if difficulty:
        query = query.filter(Content.difficulty_level == difficulty)
    if content_type:
        query = query.filter(Content.content_type == content_type)
    
    return query.all()

@router.get("/{content_id}", response_model=ContentSchema)
async def get_content(content_id: int, db: Session = Depends(get_db)):
    """Get specific content by ID."""
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.get("/{content_id}/adaptive", response_model=AdaptiveContentResponse)
async def get_adaptive_content(
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get content with adaptive format recommendations based on user's learning style."""
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Determine recommended format based on learning style
    learning_style = current_user.learning_style or "visual"  # Default to visual
    
    # Get user's interaction history with this content
    interactions = db.query(ContentInteraction).filter(
        ContentInteraction.user_id == current_user.id,
        ContentInteraction.content_id == content_id
    ).all()
    
    # Analyze format preferences from interaction history
    format_usage = {"video": 0, "audio": 0, "text": 0, "interactive": 0}
    for interaction in interactions:
        if interaction.format_used in format_usage:
            format_usage[interaction.format_used] += 1
    
    # Determine recommended format
    if learning_style == "visual":
        if content.video_url:
            recommended_format = "video"
        elif content.text_content:
            recommended_format = "text"
        else:
            recommended_format = "audio"
    elif learning_style == "auditory":
        if content.audio_url:
            recommended_format = "audio"
        elif content.video_url:
            recommended_format = "video"
        else:
            recommended_format = "text"
    else:  # kinesthetic
        if content.interactive_url:
            recommended_format = "interactive"
        elif content.video_url:
            recommended_format = "video"
        else:
            recommended_format = "text"
    
    # Override with most used format if user has strong preference
    most_used_format = max(format_usage, key=format_usage.get)
    if format_usage[most_used_format] > 2:  # If used more than twice
        recommended_format = most_used_format
    
    # Get alternative formats
    alternative_formats = []
    if content.video_url and recommended_format != "video":
        alternative_formats.append("video")
    if content.audio_url and recommended_format != "audio":
        alternative_formats.append("audio")
    if content.text_content and recommended_format != "text":
        alternative_formats.append("text")
    if content.interactive_url and recommended_format != "interactive":
        alternative_formats.append("interactive")
    
    # Generate personalization reason
    if learning_style == "visual":
        reason = "Recommended based on your visual learning preference"
    elif learning_style == "auditory":
        reason = "Recommended based on your auditory learning preference"
    else:
        reason = "Recommended based on your kinesthetic learning preference"
    
    if format_usage[most_used_format] > 2:
        reason += f" and your usage pattern (preferring {most_used_format} format)"
    
    return AdaptiveContentResponse(
        content=content,
        recommended_format=recommended_format,
        alternative_formats=alternative_formats,
        personalization_reason=reason
    )

@router.post("/{content_id}/interaction")
async def record_content_interaction(
    content_id: int,
    interaction: InteractionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record user interaction with content."""
    # Verify content exists
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Create interaction record
    db_interaction = ContentInteraction(
        user_id=current_user.id,
        content_id=content_id,
        interaction_type=interaction.interaction_type,
        format_used=interaction.format_used,
        duration_seconds=interaction.duration_seconds,
        metadata=interaction.metadata
    )
    
    db.add(db_interaction)
    db.commit()
    
    return {"message": "Interaction recorded successfully"}

@router.get("/{content_id}/progress")
async def get_content_progress(
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's progress for specific content."""
    progress = db.query(ProgressRecord).filter(
        ProgressRecord.user_id == current_user.id,
        ProgressRecord.content_id == content_id
    ).first()
    
    if not progress:
        return {
            "content_id": content_id,
            "completion_percentage": 0.0,
            "time_spent_minutes": 0,
            "last_position": 0,
            "is_completed": False,
            "quiz_score": None,
            "engagement_score": 0.0
        }
    
    return progress

@router.put("/{content_id}/progress")
async def update_content_progress(
    content_id: int,
    progress_update: ProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's progress for specific content."""
    # Verify content exists
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Get or create progress record
    progress = db.query(ProgressRecord).filter(
        ProgressRecord.user_id == current_user.id,
        ProgressRecord.content_id == content_id
    ).first()
    
    if not progress:
        progress = ProgressRecord(
            user_id=current_user.id,
            content_id=content_id
        )
        db.add(progress)
    
    # Update progress fields
    for field, value in progress_update.dict(exclude_unset=True).items():
        setattr(progress, field, value)
    
    db.commit()
    db.refresh(progress)
    
    return progress

@router.get("/recommendations/personalized", response_model=List[ContentSchema])
async def get_personalized_recommendations(
    limit: int = Query(10, description="Number of recommendations"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized content recommendations based on learning style and progress."""
    learning_style = current_user.learning_style or "visual"
    
    # Get user's completed content
    completed_content_ids = db.query(ProgressRecord.content_id).filter(
        ProgressRecord.user_id == current_user.id,
        ProgressRecord.is_completed == True
    ).all()
    completed_ids = [cid[0] for cid in completed_content_ids]
    
    # Get content that matches learning style preferences
    if learning_style == "visual":
        # Prefer video content
        query = db.query(Content).filter(
            Content.is_active == True,
            Content.video_url.isnot(None)
        )
    elif learning_style == "auditory":
        # Prefer audio content
        query = db.query(Content).filter(
            Content.is_active == True,
            Content.audio_url.isnot(None)
        )
    else:  # kinesthetic
        # Prefer interactive content
        query = db.query(Content).filter(
            Content.is_active == True,
            Content.interactive_url.isnot(None)
        )
    
    # Exclude already completed content
    if completed_ids:
        query = query.filter(~Content.id.in_(completed_ids))
    
    return query.limit(limit).all()
