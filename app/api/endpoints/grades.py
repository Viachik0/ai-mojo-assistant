from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.grade import GradeCreate, GradeUpdate, GradeResponse, GradeListResponse
from app.services.database_service import DatabaseService
from app.api.dependencies import get_db

router = APIRouter(prefix="/grades", tags=["grades"])


async def get_db_service(db: AsyncSession = Depends(get_db)) -> DatabaseService:
    """Get database service instance."""
    return DatabaseService(db)


@router.post("/", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
async def create_grade(
    grade_data: GradeCreate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Create a new grade."""
    try:
        grade = await db_service.create_grade(
            student_id=grade_data.student_id,
            teacher_id=grade_data.teacher_id,
            subject=grade_data.subject,
            grade=grade_data.grade,
            date=grade_data.date,
            lesson_topic=grade_data.lesson_topic
        )
        return grade
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create grade: {str(e)}"
        )


@router.get("/", response_model=GradeListResponse)
async def list_grades(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    days: Optional[int] = Query(None, ge=1, description="Filter grades from last N days (only with student_id)"),
    db_service: DatabaseService = Depends(get_db_service)
):
    """List grades with optional filtering and pagination."""
    try:
        if student_id:
            if days:
                grades = await db_service.get_grades_for_student(student_id=student_id, days=days)
            else:
                grades = await db_service.get_grades_for_student(student_id=student_id, days=365)  # Default to 1 year
            total = len(grades)
            grades = grades[skip:skip + limit]
        else:
            grades = await db_service.get_grades(skip=skip, limit=limit)
            all_grades = await db_service.get_grades()
            total = len(all_grades)
        
        return GradeListResponse(
            grades=grades,
            total=total,
            page=skip // limit + 1,
            per_page=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch grades: {str(e)}"
        )


@router.get("/{grade_id}", response_model=GradeResponse)
async def get_grade(
    grade_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Get grade by ID."""
    grade = await db_service.get_grade_by_id(grade_id)
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grade with ID {grade_id} not found"
        )
    return grade


@router.put("/{grade_id}", response_model=GradeResponse)
async def update_grade(
    grade_id: int,
    grade_data: GradeUpdate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Update grade by ID."""
    try:
        grade = await db_service.update_grade(
            grade_id=grade_id,
            subject=grade_data.subject,
            grade=grade_data.grade,
            date=grade_data.date,
            lesson_topic=grade_data.lesson_topic
        )
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grade with ID {grade_id} not found"
            )
        return grade
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update grade: {str(e)}"
        )


@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_grade(
    grade_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Delete grade by ID."""
    success = await db_service.delete_grade(grade_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grade with ID {grade_id} not found"
        )
