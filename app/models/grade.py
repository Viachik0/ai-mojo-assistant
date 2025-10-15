from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    subject = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)

    student = relationship("User", foreign_keys=[student_id], back_populates="grades")
    teacher = relationship("User", foreign_keys=[teacher_id])
    lesson = relationship("Lesson", back_populates="grades")

    def __repr__(self):
        return f"<Grade(value={{self.value}}, subject={{self.subject}})>"