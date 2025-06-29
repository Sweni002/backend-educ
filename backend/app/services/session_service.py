import random
import string
from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.models.participant import Participant
from app.schemas.session import SessionCreate
from fastapi_mail import MessageSchema

def generate_session_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_session(db: Session, session: SessionCreate, user_id: int):
    # Vérifie si le code existe déjà
    if db.query(SessionModel).filter(SessionModel.code == session.code).first():
        raise HTTPException(status_code=400, detail="Code already exists")

    db_session = SessionModel(
        code=session.code,
        host_id=user_id,
        title=session.title,
        description=session.description
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def join_session(db: Session, code: str, user_id: int):
    session = db.query(SessionModel).filter(SessionModel.code == code).first()
    if not session:
        return None
    
    # Vérifier si l'utilisateur n'est pas déjà dans la session
    existing_participant = db.query(Participant).filter(
        Participant.session_id == session.id,
        Participant.user_id == user_id
    ).first()
    
    if not existing_participant:
        participant = Participant(
            session_id=session.id,
            user_id=user_id
        )
        db.add(participant)
        db.commit()
    
    return session

