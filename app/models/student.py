from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, User

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_name = Column(String, nullable=False)  # e.g., "5A"

    user = relationship("User", back_populates="student_profile")

    grades = relationship("Grade", back_populates="student")

User.student_profile = relationship("Student", back_populates="user", uselist=False)
