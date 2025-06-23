from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False)
    host_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255)) 
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    host = relationship("User", back_populates="sessions")