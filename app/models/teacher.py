from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subjects = Column(JSON, nullable=False)  # List of subjects, e.g., ["Mathematics", "Physics"]

    user = relationship("User", back_populates="teacher_profile")

    grades = relationship("Grade", back_populates="teacher")
