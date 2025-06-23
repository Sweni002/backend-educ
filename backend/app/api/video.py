from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import os, shutil
from app.database import get_db
from app.models.video import Video
from app.schemas.video import VideoOut
from app.models.session import Session as SessionModel

router = APIRouter(prefix="/videos", tags=["Videos"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/{session_id}", response_model=VideoOut)
async def upload_video(session_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
     session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
     if not session:
        raise HTTPException(status_code=404, detail="Session not found")

     filename = f"{session.code}_{file.filename}"
     filepath = os.path.join(UPLOAD_DIR, filename)

     with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

     video = Video(filename=filename, file_path=filepath, session_id=session_id)
     db.add(video)
     db.commit()
     db.refresh(video)

     return video

@router.get("/session/{session_id}", response_model=VideoOut)
def get_video_by_session(session_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.session_id == session_id).first()
    if not video:
       raise HTTPException(status_code=404, detail="No video for this session")
    return video