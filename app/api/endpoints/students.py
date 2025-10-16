from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentListResponse
from app.services.database_service import DatabaseService
from app.api.dependencies import get_db

router = APIRouter(prefix="/students", tags=["students"])


async def get_db_service(db: AsyncSession = Depends(get_db)) -> DatabaseService:
    """Get database service instance."""
    return DatabaseService(db)


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    student_data: StudentCreate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Create a new student."""
    try:
        student = await db_service.create_student(
            user_id=student_data.user_id,
            class_name=student_data.class_name
        )
        return student
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create student: {str(e)}"
        )


@router.get("/", response_model=StudentListResponse)
async def list_students(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
    class_name: Optional[str] = Query(None, description="Filter by class name"),
    db_service: DatabaseService = Depends(get_db_service)
):
    """List students with optional filtering by class and pagination."""
    try:
        if class_name:
            students = await db_service.get_students_by_class(class_name)
            total = len(students)
            students = students[skip:skip + limit]
        else:
            students = await db_service.get_students(skip=skip, limit=limit)
            all_students = await db_service.get_students()
            total = len(all_students)
        
        return StudentListResponse(
            students=students,
            total=total,
            page=skip // limit + 1,
            per_page=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch students: {str(e)}"
        )


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Get student by ID."""
    student = await db_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    return student


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Update student by ID."""
    try:
        student = await db_service.update_student(
            student_id=student_id,
            class_name=student_data.class_name
        )
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update student: {str(e)}"
        )


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Delete student by ID."""
    success = await db_service.delete_student(student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
