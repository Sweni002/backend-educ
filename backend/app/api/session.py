from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.session import SessionCreate, SessionResponse, SessionJoin
from app.services.session_service import create_session, join_session
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/create", response_model=SessionResponse)
def create_new_session(
    session: SessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_session(db=db, session=session, user_id=current_user.id)


@router.post("/join", response_model=SessionResponse)
def join_existing_session(
    session_join: SessionJoin,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = join_session(db=db, code=session_join.code, user_id=current_user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session