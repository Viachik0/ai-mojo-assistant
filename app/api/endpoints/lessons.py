from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.lesson import LessonCreate, LessonUpdate, LessonResponse, LessonListResponse
from app.services.database_service import DatabaseService
from app.api.dependencies import get_db

router = APIRouter(prefix="/lessons", tags=["lessons"])


async def get_db_service(db: AsyncSession = Depends(get_db)) -> DatabaseService:
    """Get database service instance."""
    return DatabaseService(db)


@router.post("/", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    lesson_data: LessonCreate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Create a new lesson."""
    try:
        lesson = await db_service.create_lesson(
            date=lesson_data.date,
            subject=lesson_data.subject,
            class_name=lesson_data.class_name,
            teacher_id=lesson_data.teacher_id,
            topic=lesson_data.topic
        )
        return lesson
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create lesson: {str(e)}"
        )


@router.get("/", response_model=LessonListResponse)
async def list_lessons(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
    db_service: DatabaseService = Depends(get_db_service)
):
    """List lessons with pagination."""
    try:
        lessons = await db_service.get_lessons(skip=skip, limit=limit)
        all_lessons = await db_service.get_lessons()
        total = len(all_lessons)
        
        return LessonListResponse(
            lessons=lessons,
            total=total,
            page=skip // limit + 1,
            per_page=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch lessons: {str(e)}"
        )


@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson(
    lesson_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Get lesson by ID."""
    lesson = await db_service.get_lesson_by_id(lesson_id)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson with ID {lesson_id} not found"
        )
    return lesson


@router.put("/{lesson_id}", response_model=LessonResponse)
async def update_lesson(
    lesson_id: int,
    lesson_data: LessonUpdate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Update lesson by ID."""
    try:
        lesson = await db_service.update_lesson(
            lesson_id=lesson_id,
            date=lesson_data.date,
            subject=lesson_data.subject,
            class_name=lesson_data.class_name,
            topic=lesson_data.topic
        )
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lesson with ID {lesson_id} not found"
            )
        return lesson
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update lesson: {str(e)}"
        )


@router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lesson(
    lesson_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Delete lesson by ID."""
    success = await db_service.delete_lesson(lesson_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson with ID {lesson_id} not found"
        )
