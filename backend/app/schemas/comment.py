# app/schemas/comment.py
from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    message: str

class CommentCreate(CommentBase):
    session_id: int

class CommentResponse(CommentBase):
    id: int
    session_id: int
    user_id: int
    created_at: datetime
    user_name: str 
    class Config:
        from_attributes = True