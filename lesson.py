from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    topic = Column(String, nullable=False)
    class_name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    teacher = relationship("User")
    attendances = relationship("Attendance", back_populates="lesson")
    homeworks = relationship("Homework", back_populates="lesson")