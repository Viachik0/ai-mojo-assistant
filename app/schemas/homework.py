from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class HomeworkBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    due_date: datetime
    lesson_id: int
    teacher_id: int


class HomeworkCreate(HomeworkBase):
    pass


class HomeworkUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class HomeworkResponse(HomeworkBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
        


class HomeworkListResponse(BaseModel):
    homework: list[HomeworkResponse]
    total: int
    page: int
    per_page: int
