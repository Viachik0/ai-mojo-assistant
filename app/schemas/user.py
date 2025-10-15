from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


class RoleEnum(str, Enum):
    teacher = "teacher"
    parent = "parent"
    student = "student"


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    role: RoleEnum


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int
    page: int
    per_page: int
