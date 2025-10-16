from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    topic = Column(String, nullable=False)
    class_name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    teacher = relationship("User")
    grades = relationship("Grade", back_populates="lesson")

    def __repr__(self):
        return f"<Lesson(subject={{self.subject}}, date={{self.date}})>"