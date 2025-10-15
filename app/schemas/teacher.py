from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class TeacherBase(BaseModel):
    user_id: int
    subjects: List[str] = Field(..., min_length=1)


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    subjects: Optional[List[str]] = Field(None, min_length=1)


class TeacherResponse(TeacherBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TeacherListResponse(BaseModel):
    teachers: list[TeacherResponse]
    total: int
    page: int
    per_page: int
