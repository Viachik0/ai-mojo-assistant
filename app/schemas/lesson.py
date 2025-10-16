from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class LessonBase(BaseModel):
    subject: str = Field(..., min_length=1, max_length=100)
    date: datetime
    topic: str = Field(..., min_length=1, max_length=255)
    class_name: str = Field(..., min_length=1, max_length=10)
    teacher_id: int


class LessonCreate(LessonBase):
    pass


class LessonUpdate(BaseModel):
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    date: Optional[datetime] = None
    topic: Optional[str] = Field(None, min_length=1, max_length=255)
    class_name: Optional[str] = Field(None, min_length=1, max_length=10)


class LessonResponse(LessonBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
        


class LessonListResponse(BaseModel):
    lessons: list[LessonResponse]
    total: int
    page: int
    per_page: int
