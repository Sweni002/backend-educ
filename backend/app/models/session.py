from sqlalchemy import Column, Integer, String, DateTime, ForeignKey ,Boolean
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
    is_live = Column(Boolean, default=False)  # ✅ Indique si le live est en cours

    host = relationship("User", back_populates="sessions")
    video = relationship("Video", back_populates="session", uselist=False)  # one-to-one relation
