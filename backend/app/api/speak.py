from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.speak_request import SpeakRequestCreate, SpeakRequestResponse, SpeakRequestUpdate
from app.services.speak_service import create_speak_request, update_speak_request, get_session_speak_requests
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/request", response_model=SpeakRequestResponse)
def request_to_speak(
    request: SpeakRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_speak_request(db=db, request=request, user_id=current_user.id)

@router.put("/request/{request_id}", response_model=SpeakRequestResponse)
def update_speak_request_status(
    request_id: int,
    update: SpeakRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Vérifier que l'utilisateur est bien l'hôte de la session
    db_request = update_speak_request(db=db, request_id=request_id, update=update)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

@router.get("/requests/{session_id}", response_model=List[SpeakRequestResponse])
def get_speak_requests(session_id: int, db: Session = Depends(get_db)):
    return get_session_speak_requests(db=db, session_id=session_id)