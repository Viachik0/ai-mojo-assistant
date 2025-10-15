from pydantic import BaseModel, Field
from typing import Optional


class StudentBase(BaseModel):
    user_id: int
    class_name: str = Field(..., min_length=1, max_length=10)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    class_name: Optional[str] = Field(None, min_length=1, max_length=10)


class StudentResponse(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
        


class StudentListResponse(BaseModel):
    students: list[StudentResponse]
    total: int
    page: int
    per_page: int
