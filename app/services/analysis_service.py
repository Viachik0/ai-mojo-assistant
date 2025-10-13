import logging
from typing import List, Dict
from app.integrations.mojo_client import MojoClient
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self, mojo_client: MojoClient):
        self.mojo_client = mojo_client
        self.llm_service = LLMService()
    
    async def check_missing_grades(self):
        """Check for teachers with missing grades and send alerts"""
        teachers = await self.mojo_client.get_teachers()
        
        for teacher in teachers:
            missing_grades = await self.mojo_client.get_missing_grades(teacher['id'])
            if missing_grades:
                alert_data = {
                    "message": f"You have {len(missing_grades)} lessons without grades. Please grade them within 3 days."
                }
                await self.mojo_client.send_teacher_alert(teacher['id'], alert_data)
    
    async def generate_weekly_reports(self):
        """Generate and send weekly performance reports to parents"""
        students = await self.mojo_client.get_students()
        
        for student in students:
            grades = await self.mojo_client.get_grades(student['id'], days=7)
            if grades:
                report_data = await self.llm_service.analyze_performance(grades)
                await self.mojo_client.send_parent_report(student['id'], report_data)