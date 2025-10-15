from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AttendanceBase(BaseModel):
    student_id: int
    lesson_id: int
    present: bool = True
    date: datetime


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    present: Optional[bool] = None


class AttendanceResponse(AttendanceBase):
    id: int

    class Config:
        from_attributes = True


class AttendanceListResponse(BaseModel):
    attendance_records: list[AttendanceResponse]
    total: int
    page: int
    per_page: int
