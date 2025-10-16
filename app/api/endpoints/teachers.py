from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.teacher import TeacherCreate, TeacherUpdate, TeacherResponse, TeacherListResponse
from app.services.database_service import DatabaseService
from app.api.dependencies import get_db

router = APIRouter(prefix="/teachers", tags=["teachers"])


async def get_db_service(db: AsyncSession = Depends(get_db)) -> DatabaseService:
    """Get database service instance."""
    return DatabaseService(db)


@router.post("/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher(
    teacher_data: TeacherCreate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Create a new teacher."""
    try:
        teacher = await db_service.create_teacher(
            user_id=teacher_data.user_id,
            subjects=teacher_data.subjects
        )
        return teacher
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create teacher: {str(e)}"
        )


@router.get("/", response_model=TeacherListResponse)
async def list_teachers(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
    db_service: DatabaseService = Depends(get_db_service)
):
    """List teachers with pagination."""
    try:
        teachers = await db_service.get_teachers(skip=skip, limit=limit)
        all_teachers = await db_service.get_teachers()
        total = len(all_teachers)
        
        return TeacherListResponse(
            teachers=teachers,
            total=total,
            page=skip // limit + 1,
            per_page=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch teachers: {str(e)}"
        )


@router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher(
    teacher_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Get teacher by ID."""
    teacher = await db_service.get_teacher_by_id(teacher_id)
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher with ID {teacher_id} not found"
        )
    return teacher


@router.put("/{teacher_id}", response_model=TeacherResponse)
async def update_teacher(
    teacher_id: int,
    teacher_data: TeacherUpdate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Update teacher by ID."""
    try:
        teacher = await db_service.update_teacher(
            teacher_id=teacher_id,
            subjects=teacher_data.subjects
        )
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Teacher with ID {teacher_id} not found"
            )
        return teacher
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update teacher: {str(e)}"
        )


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(
    teacher_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Delete teacher by ID."""
    success = await db_service.delete_teacher(teacher_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher with ID {teacher_id} not found"
        )
