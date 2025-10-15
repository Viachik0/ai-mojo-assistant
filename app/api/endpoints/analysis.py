from fastapi import APIRouter, HTTPException, Query
from app.services.analysis_service import AnalysisService
from app.integrations.mojo_client import MojoClient
from app.core.config import settings

router = APIRouter()

# Initialize with proper configuration
mojo_client = MojoClient(settings.MOJO_BASE_URL, settings.MOJO_API_KEY)
analysis_service = AnalysisService(mojo_client)

@router.post("/analyze-grades")
async def analyze_grades(teacher_id: str):
    """Trigger grade analysis for missing grades"""
    try:
        await analysis_service.check_missing_grades()
        return {"message": "Analysis completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analytics/student/{student_id}/grades")
async def analyze_student_grades(
    student_id: int,
    days: int = Query(30, description="Number of days to analyze", ge=1, le=365)
):
    """Analyze grade trends for a student"""
    try:
        result = await analysis_service.analyze_student_grades(student_id, days)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result.get("message"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analytics/student/{student_id}/attendance")
async def analyze_student_attendance(
    student_id: int,
    days: int = Query(30, description="Number of days to analyze", ge=1, le=365)
):
    """Analyze attendance patterns for a student"""
    try:
        result = await analysis_service.analyze_student_attendance(student_id, days)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result.get("message"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analytics/student/{student_id}/homework")
async def analyze_homework_completion(
    student_id: int,
    days: int = Query(30, description="Number of days to analyze", ge=1, le=365)
):
    """Analyze homework completion for a student"""
    try:
        result = await analysis_service.analyze_homework_completion(student_id, days)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result.get("message"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analytics/student/{student_id}/comprehensive")
async def generate_comprehensive_report(
    student_id: int,
    days: int = Query(30, description="Number of days to analyze", ge=1, le=365)
):
    """Generate a comprehensive analytics report with AI insights"""
    try:
        result = await analysis_service.generate_comprehensive_report(student_id, days)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result.get("message"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))