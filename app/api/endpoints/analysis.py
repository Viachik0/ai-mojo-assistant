from fastapi import APIRouter, HTTPException
from app.services.analysis_service import AnalysisService
from app.integrations.mojo_client import MojoClient

router = APIRouter()
analysis_service = AnalysisService(MojoClient("", ""))  # Initialize properly

@router.post("/analyze-grades")
async def analyze_grades(teacher_id: str):
    try:
        await analysis_service.check_missing_grades()
        return {"message": "Analysis completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))