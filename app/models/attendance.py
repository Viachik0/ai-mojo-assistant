from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    present = Column(Boolean, default=True)
    date = Column(DateTime, nullable=False)

    student = relationship("User")
    lesson = relationship("Lesson")

    def __repr__(self):
        return f"<Attendance(student_id={{self.student_id}}, present={{self.present}})>"