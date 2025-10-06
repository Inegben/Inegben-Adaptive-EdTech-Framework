from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User, Content, ProgressRecord, ContentInteraction
from app.schemas import UserAnalytics, ContentAnalytics
from app.auth import get_current_user

router = APIRouter()

@router.get("/user/{user_id}", response_model=UserAnalytics)
async def get_user_analytics(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get comprehensive analytics for a specific user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate total time spent
    total_time = db.query(func.sum(ProgressRecord.time_spent_minutes)).filter(
        ProgressRecord.user_id == user_id
    ).scalar() or 0
    
    # Count completed content
    completed_content = db.query(func.count(ProgressRecord.id)).filter(
        ProgressRecord.user_id == user_id,
        ProgressRecord.is_completed == True
    ).scalar() or 0
    
    # Calculate average engagement
    avg_engagement = db.query(func.avg(ProgressRecord.engagement_score)).filter(
        ProgressRecord.user_id == user_id
    ).scalar() or 0.0
    
    # Get preferred format from interactions
    format_preferences = db.query(
        ContentInteraction.format_used,
        func.count(ContentInteraction.id).label('count')
    ).filter(
        ContentInteraction.user_id == user_id
    ).group_by(ContentInteraction.format_used).all()
    
    preferred_format = "video"  # default
    if format_preferences:
        preferred_format = max(format_preferences, key=lambda x: x.count).format_used
    
    # Get progress trend (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    progress_trend = db.query(
        func.date(ProgressRecord.updated_at).label('date'),
        func.count(ProgressRecord.id).label('activities'),
        func.avg(ProgressRecord.completion_percentage).label('avg_completion')
    ).filter(
        ProgressRecord.user_id == user_id,
        ProgressRecord.updated_at >= thirty_days_ago
    ).group_by(func.date(ProgressRecord.updated_at)).order_by('date').all()
    
    trend_data = [
        {
            "date": str(record.date),
            "activities": record.activities,
            "avg_completion": float(record.avg_completion or 0)
        }
        for record in progress_trend
    ]
    
    return UserAnalytics(
        user_id=user_id,
        total_time_spent=total_time,
        content_completed=completed_content,
        average_engagement=float(avg_engagement),
        preferred_format=preferred_format,
        learning_style=user.learning_style or "unknown",
        progress_trend=trend_data
    )

@router.get("/content/{content_id}", response_model=ContentAnalytics)
async def get_content_analytics(
    content_id: int,
    db: Session = Depends(get_db)
):
    """Get comprehensive analytics for specific content."""
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Count total views
    total_views = db.query(func.count(ContentInteraction.id)).filter(
        ContentInteraction.content_id == content_id,
        ContentInteraction.interaction_type == "view"
    ).scalar() or 0
    
    # Calculate completion rate
    total_started = db.query(func.count(ProgressRecord.id)).filter(
        ProgressRecord.content_id == content_id
    ).scalar() or 0
    
    total_completed = db.query(func.count(ProgressRecord.id)).filter(
        ProgressRecord.content_id == content_id,
        ProgressRecord.is_completed == True
    ).scalar() or 0
    
    completion_rate = (total_completed / total_started * 100) if total_started > 0 else 0
    
    # Calculate average engagement
    avg_engagement = db.query(func.avg(ProgressRecord.engagement_score)).filter(
        ProgressRecord.content_id == content_id
    ).scalar() or 0.0
    
    # Get format preferences
    format_preferences = db.query(
        ContentInteraction.format_used,
        func.count(ContentInteraction.id).label('count')
    ).filter(
        ContentInteraction.content_id == content_id
    ).group_by(ContentInteraction.format_used).all()
    
    format_prefs = {fp.format_used: fp.count for fp in format_preferences}
    
    # Get user feedback (quiz scores)
    quiz_scores = db.query(ProgressRecord.quiz_score).filter(
        ProgressRecord.content_id == content_id,
        ProgressRecord.quiz_score.isnot(None)
    ).all()
    
    avg_quiz_score = 0
    if quiz_scores:
        scores = [score[0] for score in quiz_scores if score[0] is not None]
        avg_quiz_score = sum(scores) / len(scores) if scores else 0
    
    feedback_data = {
        "average_quiz_score": avg_quiz_score,
        "total_quiz_attempts": len(quiz_scores),
        "completion_rate": completion_rate
    }
    
    return ContentAnalytics(
        content_id=content_id,
        total_views=total_views,
        completion_rate=completion_rate,
        average_engagement=float(avg_engagement),
        format_preferences=format_prefs,
        user_feedback=feedback_data
    )

@router.get("/dashboard/overview")
async def get_dashboard_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get overview analytics for the current user's dashboard."""
    user_id = current_user.id
    
    # Basic stats
    total_time = db.query(func.sum(ProgressRecord.time_spent_minutes)).filter(
        ProgressRecord.user_id == user_id
    ).scalar() or 0
    
    completed_content = db.query(func.count(ProgressRecord.id)).filter(
        ProgressRecord.user_id == user_id,
        ProgressRecord.is_completed == True
    ).scalar() or 0
    
    in_progress = db.query(func.count(ProgressRecord.id)).filter(
        ProgressRecord.user_id == user_id,
        ProgressRecord.is_completed == False,
        ProgressRecord.completion_percentage > 0
    ).scalar() or 0
    
    # Recent activity (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_activity = db.query(
        func.date(ProgressRecord.updated_at).label('date'),
        func.count(ProgressRecord.id).label('activities')
    ).filter(
        ProgressRecord.user_id == user_id,
        ProgressRecord.updated_at >= seven_days_ago
    ).group_by(func.date(ProgressRecord.updated_at)).order_by(desc('date')).limit(7).all()
    
    # Learning style distribution (if user has completed assessment)
    learning_style = current_user.learning_style
    
    # Format usage statistics
    format_usage = db.query(
        ContentInteraction.format_used,
        func.count(ContentInteraction.id).label('count')
    ).filter(
        ContentInteraction.user_id == user_id
    ).group_by(ContentInteraction.format_used).all()
    
    format_stats = {fu.format_used: fu.count for fu in format_usage}
    
    return {
        "user_id": user_id,
        "learning_style": learning_style,
        "total_time_minutes": total_time,
        "content_completed": completed_content,
        "content_in_progress": in_progress,
        "recent_activity": [
            {
                "date": str(activity.date),
                "activities": activity.activities
            }
            for activity in recent_activity
        ],
        "format_usage": format_stats,
        "assessment_completed": current_user.assessment_completed
    }

@router.get("/learning-styles/distribution")
async def get_learning_style_distribution(db: Session = Depends(get_db)):
    """Get distribution of learning styles across all users."""
    distribution = db.query(
        User.learning_style,
        func.count(User.id).label('count')
    ).filter(
        User.learning_style.isnot(None),
        User.assessment_completed == True
    ).group_by(User.learning_style).all()
    
    return {
        "distribution": [
            {
                "learning_style": dist.learning_style,
                "count": dist.count
            }
            for dist in distribution
        ],
        "total_assessed_users": sum(dist.count for dist in distribution)
    }
