from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class Role(enum.Enum):
    teacher = "teacher"
    parent = "parent"
    student = "student"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(Role), nullable=False)

    # Relationships
    student_profile = relationship("Student", back_populates="user", uselist=False)
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User(name={self.name}, email={self.email}, role={self.role})>"
