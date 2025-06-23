from pydantic import BaseModel
from datetime import datetime

class TranscriptionBase(BaseModel):
    text_content: str

class TranscriptionCreate(TranscriptionBase):
    session_id: int

class TranscriptionResponse(TranscriptionBase):
    id: int
    session_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True