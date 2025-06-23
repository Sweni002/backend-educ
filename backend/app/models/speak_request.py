from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class SpeakStatusEnum(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class SpeakRequest(Base):
    __tablename__ = "speak_requests"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(SpeakStatusEnum), default=SpeakStatusEnum.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="speak_requests")
    session = relationship("Session", backref="speak_requests")
