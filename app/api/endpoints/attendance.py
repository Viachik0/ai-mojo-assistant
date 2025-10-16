from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse, AttendanceListResponse
from app.services.database_service import DatabaseService
from app.api.dependencies import get_db
from datetime import datetime

router = APIRouter(prefix="/attendance", tags=["attendance"])


async def get_db_service(db: AsyncSession = Depends(get_db)) -> DatabaseService:
    """Get database service instance."""
    return DatabaseService(db)


@router.post("/", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def mark_attendance(
    attendance_data: AttendanceCreate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Mark attendance for a student in a lesson."""
    try:
        attendance = await db_service.mark_attendance(
            student_id=attendance_data.student_id,
            lesson_id=attendance_data.lesson_id,
            present=attendance_data.present
        )
        return attendance
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to mark attendance: {str(e)}"
        )


@router.get("/", response_model=AttendanceListResponse)
async def list_attendance(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
    db_service: DatabaseService = Depends(get_db_service)
):
    """List attendance records with pagination."""
    try:
        attendance_records = await db_service.get_attendance_records(skip=skip, limit=limit)
        all_records = await db_service.get_attendance_records()
        total = len(all_records)
        
        return AttendanceListResponse(
            attendance_records=attendance_records,
            total=total,
            page=skip // limit + 1,
            per_page=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch attendance records: {str(e)}"
        )


@router.get("/{attendance_id}", response_model=AttendanceResponse)
async def get_attendance(
    attendance_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Get attendance record by ID."""
    attendance = await db_service.get_attendance_by_id(attendance_id)
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance record with ID {attendance_id} not found"
        )
    return attendance


@router.put("/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance(
    attendance_id: int,
    attendance_data: AttendanceUpdate,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Update attendance record by ID."""
    try:
        attendance = await db_service.update_attendance(
            attendance_id=attendance_id,
            present=attendance_data.present
        )
        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance record with ID {attendance_id} not found"
            )
        return attendance
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update attendance: {str(e)}"
        )


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attendance(
    attendance_id: int,
    db_service: DatabaseService = Depends(get_db_service)
):
    """Delete attendance record by ID."""
    success = await db_service.delete_attendance(attendance_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance record with ID {attendance_id} not found"
        )
