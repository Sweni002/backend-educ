from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VideoBase(BaseModel):
      filename: str
      file_path: str

class VideoCreate(VideoBase):
      session_id: int

class VideoOut(VideoBase):
      id: int
      uploaded_at: datetime
      session_id: int

class Config:
      orm_mode = True