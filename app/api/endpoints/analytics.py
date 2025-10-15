from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.database_service import DatabaseService
from app.api.dependencies import get_db
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["analytics"])


async def get_db_service(db: AsyncSession = Depends(get_db)) -> DatabaseService:
    """Get database service instance."""
    return DatabaseService(db)


@router.get("/student/{student_id}/grades-summary")
async def get_student_grades_summary(
    student_id: int,
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db_service: DatabaseService = Depends(get_db_service)
) -> Dict[str, Any]:
    """
    Get summary of grades for a specific student over a period.
    Returns grade count, average, and subject breakdown.
    """
    try:
        # Check if student exists
        student = await db_service.get_student_by_id(student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        
        # Get grades for the period
        grades = await db_service.get_grades_for_student(student_id, days=days)
        
        if not grades:
            return {
                "student_id": student_id,
                "period_days": days,
                "total_grades": 0,
                "subjects": {},
                "message": "No grades found for this period"
            }
        
        # Analyze grades by subject
        subject_stats = {}
        for grade in grades:
            subject = grade.subject
            if subject not in subject_stats:
                subject_stats[subject] = {
                    "count": 0,
                    "grades": []
                }
            subject_stats[subject]["count"] += 1
            subject_stats[subject]["grades"].append(grade.grade)
        
        return {
            "student_id": student_id,
            "period_days": days,
            "total_grades": len(grades),
            "subjects": subject_stats,
            "date_range": {
                "from": (datetime.now() - timedelta(days=days)).isoformat(),
                "to": datetime.now().isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate grade summary: {str(e)}"
        )


@router.get("/class/{class_name}/overview")
async def get_class_overview(
    class_name: str,
    db_service: DatabaseService = Depends(get_db_service)
) -> Dict[str, Any]:
    """
    Get overview of a class including student count and recent activity.
    """
    try:
        students = await db_service.get_students_by_class(class_name)
        
        if not students:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No students found in class {class_name}"
            )
        
        # Get recent grades for all students in the class
        all_grades = []
        for student in students:
            grades = await db_service.get_grades_for_student(student.id, days=7)
            all_grades.extend(grades)
        
        return {
            "class_name": class_name,
            "student_count": len(students),
            "recent_grades_count": len(all_grades),
            "students": [
                {
                    "id": s.id,
                    "user_id": s.user_id
                } for s in students
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate class overview: {str(e)}"
        )


@router.get("/reports/summary")
async def get_system_summary(
    db_service: DatabaseService = Depends(get_db_service)
) -> Dict[str, Any]:
    """
    Get overall system summary including counts of users, students, teachers, etc.
    """
    try:
        users = await db_service.get_users()
        students = await db_service.get_students()
        teachers = await db_service.get_teachers()
        grades = await db_service.get_grades()
        lessons = await db_service.get_lessons()
        
        return {
            "summary": {
                "total_users": len(users),
                "total_students": len(students),
                "total_teachers": len(teachers),
                "total_grades": len(grades),
                "total_lessons": len(lessons)
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate system summary: {str(e)}"
        )
