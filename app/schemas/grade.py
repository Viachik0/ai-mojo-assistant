from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GradeBase(BaseModel):
    student_id: int
    teacher_id: int
    subject: str = Field(..., min_length=1, max_length=100)
    grade: str = Field(..., min_length=1, max_length=10)
    date: datetime
    lesson_topic: Optional[str] = Field(None, max_length=255)


class GradeCreate(GradeBase):
    pass


class GradeUpdate(BaseModel):
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    grade: Optional[str] = Field(None, min_length=1, max_length=10)
    date: Optional[datetime] = None
    lesson_topic: Optional[str] = Field(None, max_length=255)


class GradeResponse(GradeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
        


class GradeListResponse(BaseModel):
    grades: list[GradeResponse]
    total: int
    page: int
    per_page: int
