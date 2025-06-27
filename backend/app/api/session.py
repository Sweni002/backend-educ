from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.session import SessionCreate, SessionResponse, SessionJoin
from app.services.session_service import create_session, join_session
from app.api.auth import get_current_user
from app.models.user import User
from app.api.auth import get_current_user
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.models.session import Session as SessionModel
from app.services.session_service import generate_session_code

router = APIRouter()


conf = ConnectionConfig(
    MAIL_USERNAME="niseynwa@gmail.com",
    MAIL_PASSWORD="hlpt maub nktj bsrt ",
    MAIL_FROM="niseynwa@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,       # remplace MAIL_TLS
    MAIL_SSL_TLS=False,       # nouveau champ obligatoire
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

@router.get("/generate-code")
def generate_code():
    return {"code": generate_session_code()}

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

@router.post("/{session_id}/send_code")
async def send_session_code(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    users = db.query(User).all()
    emails = [user.email for user in users if user.email]

    if not emails:
        raise HTTPException(status_code=404, detail="No users with emails found")

    fm = FastMail(conf)

    for email in emails:
        body = f"Bonjour,\n\nLe code de la session '{session.title}' est : {session.code}\n\nEnvoyé par : {current_user.email}\n\nCordialement."
        message = MessageSchema(
            subject="Code de session",
            recipients=[email],
            body=body,
            subtype="plain"
        )
        await fm.send_message(message)

    return {"message": f"Code de session envoyé à {len(emails)} utilisateurs depuis {current_user.email}."}


@router.get("/by-code/{code}", response_model=SessionResponse)
def get_session_by_code(
         code: str,
         db: Session = Depends(get_db)
      ):
    session = db.query(SessionModel).filter(SessionModel.code == code).first()
    if not session:
           raise HTTPException(status_code=404, detail="Session not found")
    return session