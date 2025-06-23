from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.comment_service import create_comment, get_session_comments
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=CommentResponse)
def add_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_comment(db=db, comment=comment, user_id=current_user.id)

@router.get("/{session_id}", response_model=List[CommentResponse])
def get_comments(session_id: int, db: Session = Depends(get_db)):
    return get_session_comments(db=db, session_id=session_id)