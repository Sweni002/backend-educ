from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SessionBase(BaseModel):
    title: Optional[str] = None
    description : Optional[str] = None

class SessionCreate(SessionBase):
    pass

class SessionResponse(SessionBase):
    id: int
    code: str
    description :str
    host_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SessionJoin(BaseModel):
    code: str