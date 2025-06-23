from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.file import FileResponse
from app.services.file_service import save_file, get_session_files
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/upload/{session_id}", response_model=FileResponse)
def upload_file(
    session_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return save_file(file=file, session_id=session_id, user_id=current_user.id, db=db)

@router.get("/{session_id}", response_model=List[FileResponse])
def get_files(session_id: int, db: Session = Depends(get_db)):
    return get_session_files(db=db, session_id=session_id)