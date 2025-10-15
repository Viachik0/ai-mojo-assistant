from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse, RoleEnum
from app.services.database_service import DatabaseService
from app.api.dependencies import get_db
from app.models.user import Role

router = APIRouter(prefix="/users", tags=["users"])


async def get_db_service(db: AsyncSession = Depends(get_db)) -> DatabaseService:
    """Get database service instance."""
    return DatabaseService(db)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Create a new user."""
    try:
        role = Role[user_data.role.value]
        user = await db_service.create_user(
            name=user_data.name,
            email=user_data.email,
            role=role
        )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create user: {str(e)}"
        )


@router.get("/", response_model=UserListResponse)
async def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
    role: Optional[RoleEnum] = Query(None, description="Filter by role"),
    db_service: DatabaseService = Depends(get_db_service)
):
    """List users with optional filtering by role and pagination."""
    try:
        if role:
            role_enum = Role[role.value]
            users = await db_service.get_users_by_role(role_enum)
            # Apply pagination manually for filtered results
            total = len(users)
            users = users[skip:skip + limit]
        else:
            users = await db_service.get_users(skip=skip, limit=limit)
            # Get total count (this is a simplified version, in production you'd want a proper count query)
            all_users = await db_service.get_users()
            total = len(all_users)
        
        return UserListResponse(
            users=users,
            total=total,
            page=skip // limit + 1,
            per_page=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch users: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Get user by ID."""
    user = await db_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Update user by ID."""
    try:
        role = Role[user_data.role.value] if user_data.role else None
        user = await db_service.update_user(
            user_id=user_id,
            name=user_data.name,
            email=user_data.email,
            role=role
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update user: {str(e)}"
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Delete user by ID."""
    success = await db_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
