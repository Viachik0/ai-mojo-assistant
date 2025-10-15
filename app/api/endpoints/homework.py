from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.homework import HomeworkCreate, HomeworkUpdate, HomeworkResponse, HomeworkListResponse
from app.services.database_service import DatabaseService
from app.api.dependencies import get_db

router = APIRouter(prefix="/homework", tags=["homework"])


async def get_db_service(db: AsyncSession = Depends(get_db)) -> DatabaseService:
    """Get database service instance."""
    return DatabaseService(db)


@router.post("/", response_model=HomeworkResponse, status_code=status.HTTP_201_CREATED)
async def create_homework(
    homework_data: HomeworkCreate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Create new homework assignment."""
    try:
        homework = await db_service.create_homework(
            lesson_id=homework_data.lesson_id,
            title=homework_data.title,
            description=homework_data.description,
            due_date=homework_data.due_date,
            teacher_id=homework_data.teacher_id
        )
        return homework
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create homework: {str(e)}"
        )


@router.get("/", response_model=HomeworkListResponse)
async def list_homework(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
    db_service: DatabaseService = Depends(get_db_service)
):
    """List homework assignments with pagination."""
    try:
        homework = await db_service.get_homework_list(skip=skip, limit=limit)
        all_homework = await db_service.get_homework_list()
        total = len(all_homework)
        
        return HomeworkListResponse(
            homework=homework,
            total=total,
            page=skip // limit + 1,
            per_page=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch homework: {str(e)}"
        )


@router.get("/{homework_id}", response_model=HomeworkResponse)
async def get_homework(
    homework_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Get homework assignment by ID."""
    homework = await db_service.get_homework_by_id(homework_id)
    if not homework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Homework with ID {homework_id} not found"
        )
    return homework


@router.put("/{homework_id}", response_model=HomeworkResponse)
async def update_homework(
    homework_id: int,
    homework_data: HomeworkUpdate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Update homework assignment by ID."""
    try:
        homework = await db_service.update_homework(
            homework_id=homework_id,
            title=homework_data.title,
            description=homework_data.description,
            due_date=homework_data.due_date
        )
        if not homework:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Homework with ID {homework_id} not found"
            )
        return homework
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update homework: {str(e)}"
        )


@router.delete("/{homework_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_homework(
    homework_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Delete homework assignment by ID."""
    success = await db_service.delete_homework(homework_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Homework with ID {homework_id} not found"
        )
