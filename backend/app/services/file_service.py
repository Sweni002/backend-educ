import os
import uuid
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.file import File
from app.schemas.file import FileCreate

UPLOAD_DIR = "uploads"

def save_file(file: UploadFile, session_id: int, user_id: int, db: Session):
    # Créer le dossier uploads s'il n'existe pas
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Générer un nom de fichier unique
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Sauvegarder le fichier
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    # Enregistrer en base de données
    db_file = File(
        session_id=session_id,
        user_id=user_id,
        filename=file.filename,
        file_path=file_path
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return db_file

def get_session_files(db: Session, session_id: int):
    return db.query(File).filter(File.session_id == session_id).all()