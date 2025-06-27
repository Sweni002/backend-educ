from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("Session", back_populates="video")
