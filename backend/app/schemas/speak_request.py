from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class SpeakRequestBase(BaseModel):
    session_id: int

class SpeakRequestCreate(SpeakRequestBase):
    pass

class SpeakRequestResponse(SpeakRequestBase):
    id: int
    user_id: int
    status: Literal['pending', 'accepted', 'rejected']
    created_at: datetime
    
    class Config:
        from_attributes = True

class SpeakRequestUpdate(BaseModel):
    status: Literal['accepted', 'rejected']