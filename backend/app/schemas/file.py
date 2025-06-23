from pydantic import BaseModel
from datetime import datetime

class FileBase(BaseModel):
    filename: str

class FileCreate(FileBase):
    session_id: int
    file_path: str

class FileResponse(FileBase):
    id: int
    session_id: int
    user_id: int
    file_path: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True