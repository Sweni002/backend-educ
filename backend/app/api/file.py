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


# ✅ Upload de plusieurs fichiers
@router.post("/upload-multiple/{session_id}", response_model=List[FileResponse])
def upload_multiple_files(
    session_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return [save_file(file=f, session_id=session_id, user_id=current_user.id, db=db) for f in files]


@router.get("/{session_id}", response_model=List[FileResponse])
def get_files(session_id: int, db: Session = Depends(get_db)):
    return get_session_files(db=db, session_id=session_id)


@router.get("/{session_id}")
def get_files_for_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    files = db.query(FileModel).filter(FileModel.session_id == session_id).all()
    if not files:
        return []
    # Retourner les infos nécessaires côté front (id, filename, file_path)
    return [
        {"id": f.id, "filename": f.filename, "file_path": f.file_path}
        for f in files
    ]


