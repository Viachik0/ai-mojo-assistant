from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.services.database_service import DatabaseService
from app.core.database import get_db
from app.schemas.user import UserResponse, UserCreate, UserListResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new user.
    """
    db_service = DatabaseService(db)
    created_user = await db_service.create_user(user.name, user.email, user.role)
    if not created_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return created_user

@router.get("", response_model=UserListResponse)
async def list_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve users.
    """
    db_service = DatabaseService(db)
    users = await db_service.get_users(skip=skip, limit=limit)
    return UserListResponse(
        users=users,
        total=len(users),
        page=skip // limit + 1 if limit > 0 else 1,
        per_page=limit
    )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a single user by ID.
    """
    db_service = DatabaseService(db)
    db_user = await db_service.get_user_by_id(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
