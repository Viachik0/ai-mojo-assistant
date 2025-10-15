from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class HomeworkSubmission(Base):
    __tablename__ = 'homework_submissions'

    id = Column(Integer, primary_key=True, index=True)
    homework_id = Column(Integer, ForeignKey('homework.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    submitted_at = Column(DateTime)
    content = Column(Text)
    grade = Column(Integer)
    feedback = Column(Text)
    is_completed = Column(Boolean, default=False)

    homework = relationship("Homework")
    student = relationship("User")

    def __repr__(self):
        return f"<HomeworkSubmission(homework_id={self.homework_id}, student_id={self.student_id}, completed={self.is_completed})>"
