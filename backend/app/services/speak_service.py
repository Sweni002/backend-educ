from sqlalchemy.orm import Session
from app.models.speak_request import SpeakRequest
from app.schemas.speak_request import SpeakRequestCreate, SpeakRequestUpdate

def create_speak_request(db: Session, request: SpeakRequestCreate, user_id: int):
    # Vérifier s'il n'y a pas déjà une demande en attente
    existing_request = db.query(SpeakRequest).filter(
        SpeakRequest.session_id == request.session_id,
        SpeakRequest.user_id == user_id,
        SpeakRequest.status == 'pending'
    ).first()
    
    if existing_request:
        return existing_request
    
    db_request = SpeakRequest(
        session_id=request.session_id,
        user_id=user_id
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def update_speak_request(db: Session, request_id: int, update: SpeakRequestUpdate):
    db_request = db.query(SpeakRequest).filter(SpeakRequest.id == request_id).first()
    if db_request:
        db_request.status = update.status
        db.commit()
        db.refresh(db_request)
    return db_request

def get_session_speak_requests(db: Session, session_id: int):
    return db.query(SpeakRequest).filter(
        SpeakRequest.session_id == session_id,
        SpeakRequest.status == 'pending'
    ).all()