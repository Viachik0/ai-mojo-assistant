from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    subject = Column(String, nullable=False)
    grade = Column(String, nullable=False)  # e.g., "5", "4+", etc.
    date = Column(DateTime, nullable=False)
    lesson_topic = Column(String, nullable=True)

    student = relationship("Student", back_populates="grades")
    teacher = relationship("Teacher", back_populates="grades")