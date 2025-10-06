from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User, AssessmentQuestion
from app.schemas import AssessmentQuestion as AssessmentQuestionSchema, AssessmentSubmission, AssessmentResult
from app.auth import get_current_user

router = APIRouter()

# Pre-defined assessment questions based on the specification
ASSESSMENT_QUESTIONS = [
    {
        "question_text": "When learning a new software, you prefer to:",
        "visual_answer": "Watch a video tutorial.",
        "auditory_answer": "Listen to a podcast explaining the features.",
        "kinesthetic_answer": "Click around and try to figure it out yourself."
    },
    {
        "question_text": "When you get directions to a new place, you're most likely to remember them by:",
        "visual_answer": "Picturing a map in your head.",
        "auditory_answer": "Hearing the directions repeated to you.",
        "kinesthetic_answer": "Driving there once to get a feel for the route."
    },
    {
        "question_text": "You're trying to learn a new song. You will:",
        "visual_answer": "Read the sheet music.",
        "auditory_answer": "Listen to the song repeatedly.",
        "kinesthetic_answer": "Play the tune on an instrument."
    },
    {
        "question_text": "When you read, you often find yourself:",
        "visual_answer": "Picturing the scenes in your mind.",
        "auditory_answer": "Reading out loud or mouthing the words.",
        "kinesthetic_answer": "Pacing or fidgeting to stay engaged."
    },
    {
        "question_text": "When a teacher or speaker presents a new idea, you're most engaged by:",
        "visual_answer": "Diagrams, charts, and slides.",
        "auditory_answer": "A clear, spoken explanation.",
        "kinesthetic_answer": "Hands-on examples or group activities."
    },
    {
        "question_text": "To remember a grocery list, you would:",
        "visual_answer": "Visualize the items in your cart.",
        "auditory_answer": "Repeat the list to yourself.",
        "kinesthetic_answer": "Write it down."
    },
    {
        "question_text": "When explaining something, you tend to:",
        "visual_answer": "Draw a picture or a diagram.",
        "auditory_answer": "Talk through the steps.",
        "kinesthetic_answer": "Use your hands and body language."
    },
    {
        "question_text": "In a classroom, you prefer to sit:",
        "visual_answer": "Where you can clearly see the board and the instructor's gestures.",
        "auditory_answer": "Anywhere you can hear well, even if you can't see the board.",
        "kinesthetic_answer": "Where you can stand up or move around if needed."
    },
    {
        "question_text": "Your favorite way to learn a new skill is by:",
        "visual_answer": "Watching an expert perform it.",
        "auditory_answer": "Being given detailed verbal instructions.",
        "kinesthetic_answer": "Trying it out yourself with tools or materials."
    },
    {
        "question_text": "When doing research, you prefer to get your information from:",
        "visual_answer": "Infographics or well-designed websites.",
        "auditory_answer": "Podcasts or radio documentaries.",
        "kinesthetic_answer": "Interactive simulations or hands-on tutorials."
    }
]

@router.get("/questions", response_model=List[AssessmentQuestionSchema])
async def get_assessment_questions(db: Session = Depends(get_db)):
    """Get all assessment questions for the learning style assessment."""
    # Check if questions exist in database, if not create them
    existing_questions = db.query(AssessmentQuestion).count()
    if existing_questions == 0:
        # Create questions in database
        for i, question_data in enumerate(ASSESSMENT_QUESTIONS):
            db_question = AssessmentQuestion(
                id=i + 1,
                question_text=question_data["question_text"],
                visual_answer=question_data["visual_answer"],
                auditory_answer=question_data["auditory_answer"],
                kinesthetic_answer=question_data["kinesthetic_answer"]
            )
            db.add(db_question)
        db.commit()
    
    # Return questions from database
    questions = db.query(AssessmentQuestion).filter(AssessmentQuestion.is_active == True).all()
    return questions

@router.post("/submit", response_model=AssessmentResult)
async def submit_assessment(
    submission: AssessmentSubmission,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit assessment answers and calculate learning style."""
    if len(submission.answers) != 10:
        raise HTTPException(status_code=400, detail="Assessment must have exactly 10 answers")
    
    # Calculate scores for each learning style
    scores = {"visual": 0, "auditory": 0, "kinesthetic": 0}
    
    for answer in submission.answers:
        if answer.answer in scores:
            scores[answer.answer] += 1
        else:
            raise HTTPException(status_code=400, detail=f"Invalid answer: {answer.answer}")
    
    # Determine primary learning style
    learning_style = max(scores, key=scores.get)
    
    # Calculate confidence (how clear the preference is)
    total_score = sum(scores.values())
    max_score = max(scores.values())
    confidence = max_score / total_score if total_score > 0 else 0.33
    
    # Update user profile
    current_user.learning_style = learning_style
    current_user.assessment_completed = True
    current_user.assessment_score = scores
    
    db.commit()
    
    return AssessmentResult(
        learning_style=learning_style,
        scores=scores,
        confidence=confidence
    )

@router.get("/result", response_model=AssessmentResult)
async def get_assessment_result(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the current user's assessment result."""
    if not current_user.assessment_completed:
        raise HTTPException(status_code=404, detail="Assessment not completed")
    
    if not current_user.assessment_score:
        raise HTTPException(status_code=404, detail="Assessment scores not found")
    
    # Calculate confidence
    scores = current_user.assessment_score
    total_score = sum(scores.values())
    max_score = max(scores.values())
    confidence = max_score / total_score if total_score > 0 else 0.33
    
    return AssessmentResult(
        learning_style=current_user.learning_style,
        scores=scores,
        confidence=confidence
    )

@router.post("/reset")
async def reset_assessment(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reset the user's assessment to allow retaking."""
    current_user.learning_style = None
    current_user.assessment_completed = False
    current_user.assessment_score = None
    
    db.commit()
    
    return {"message": "Assessment reset successfully"}
