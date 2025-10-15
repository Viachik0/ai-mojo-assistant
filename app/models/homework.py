from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Homework(Base):
    __tablename__ = 'homework'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    due_date = Column(DateTime, nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    lesson = relationship("Lesson")
    teacher = relationship("User")

    def __repr__(self):
        return f"<Homework(title={{self.title}}, due_date={{self.due_date}})>"