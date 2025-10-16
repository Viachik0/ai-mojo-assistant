import logging
from typing import List, Dict, Optional
from app.integrations.mojo_client import MojoClient
from app.services.llm_service import LLMService
from app.services.database_service import DatabaseService
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self, mojo_client: MojoClient, session: Optional[AsyncSession] = None):
        self.mojo_client = mojo_client
        self.llm_service = LLMService()
        self.db_service = DatabaseService(session)
    
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
                report_data = await self.llm_service.analyze_performance(
                    grades, 
                    student.get('name', 'Student')
                )
                await self.mojo_client.send_parent_report(student['id'], report_data)
    
    async def analyze_student_grades(self, student_id: int, days: int = 30) -> Dict:
        """Analyze grade trends for a student across all subjects"""
        try:
            # Get all grades for the student
            grades = await self.db_service.get_grades_by_student(student_id, days)
            
            if not grades:
                return {
                    "student_id": student_id,
                    "status": "no_data",
                    "message": "No grade data available for analysis"
                }
            
            # Group by subject and analyze trends
            subjects = set(g["subject"] for g in grades)
            grade_trends = {}
            
            for subject in subjects:
                trend_data = await self.db_service.get_grade_trends(student_id, subject, days)
                grade_trends[subject] = trend_data
            
            # Calculate overall statistics
            all_values = [g["value"] for g in grades]
            average_grade = sum(all_values) / len(all_values) if all_values else 0
            
            return {
                "student_id": student_id,
                "status": "success",
                "average_grade": round(average_grade, 2),
                "grade_trends": grade_trends,
                "total_grades": len(grades),
                "subjects_count": len(subjects)
            }
        except Exception as e:
            logger.error(f"Error analyzing student grades: {e}")
            return {
                "student_id": student_id,
                "status": "error",
                "message": str(e)
            }
    
    async def analyze_student_attendance(self, student_id: int, days: int = 30) -> Dict:
        """Analyze attendance patterns for a student"""
        try:
            attendance_stats = await self.db_service.get_attendance_stats(student_id, days)
            
            # Check for concerning patterns
            attendance_rate = attendance_stats.get("attendance_rate", 0)
            alerts = []
            
            if attendance_rate < 75:
                alert_data = await self.llm_service.generate_alert(
                    "low_attendance",
                    {"attendance_rate": attendance_rate}
                )
                alerts.append(alert_data.get("alert"))
            
            return {
                "student_id": student_id,
                "status": "success",
                "attendance_stats": attendance_stats,
                "alerts": alerts
            }
        except Exception as e:
            logger.error(f"Error analyzing student attendance: {e}")
            return {
                "student_id": student_id,
                "status": "error",
                "message": str(e)
            }
    
    async def analyze_homework_completion(self, student_id: int, days: int = 30) -> Dict:
        """Analyze homework completion trends for a student"""
        try:
            homework_stats = await self.db_service.get_homework_completion_rate(student_id, days)
            
            # Check for alerts
            alerts = []
            overdue_count = homework_stats.get("overdue_count", 0)
            
            if overdue_count > 2:
                alert_data = await self.llm_service.generate_alert(
                    "missing_homework",
                    {"overdue_count": overdue_count}
                )
                alerts.append(alert_data.get("alert"))
            
            return {
                "student_id": student_id,
                "status": "success",
                "homework_stats": homework_stats,
                "alerts": alerts
            }
        except Exception as e:
            logger.error(f"Error analyzing homework completion: {e}")
            return {
                "student_id": student_id,
                "status": "error",
                "message": str(e)
            }
    
    async def generate_comprehensive_report(self, student_id: int, days: int = 30) -> Dict:
        """Generate a comprehensive analytics report with AI insights"""
        try:
            # Gather all analytics data
            grades_analysis = await self.analyze_student_grades(student_id, days)
            attendance_analysis = await self.analyze_student_attendance(student_id, days)
            homework_analysis = await self.analyze_homework_completion(student_id, days)
            
            # Prepare data for AI insights
            analytics_data = {
                "grade_trends": grades_analysis.get("grade_trends", {}),
                "attendance": attendance_analysis.get("attendance_stats", {}),
                "homework": homework_analysis.get("homework_stats", {})
            }
            
            # Generate AI insights
            insights = await self.llm_service.generate_insights(analytics_data)
            
            # Generate recommendations
            student_profile = {
                "average_grade": grades_analysis.get("average_grade", 0),
                "attendance_rate": attendance_analysis.get("attendance_stats", {}).get("attendance_rate", 0),
                "homework_completion": homework_analysis.get("homework_stats", {}).get("completion_rate", 0),
                "strengths": self._identify_strengths(grades_analysis),
                "areas_for_improvement": self._identify_improvements(grades_analysis, attendance_analysis, homework_analysis)
            }
            
            recommendations = await self.llm_service.generate_recommendations(student_profile)
            
            return {
                "student_id": student_id,
                "status": "success",
                "period_days": days,
                "grades": grades_analysis,
                "attendance": attendance_analysis,
                "homework": homework_analysis,
                "ai_insights": insights.get("insights"),
                "recommendations": recommendations.get("recommendations")
            }
        except Exception as e:
            logger.error(f"Error generating comprehensive report: {e}")
            return {
                "student_id": student_id,
                "status": "error",
                "message": str(e)
            }
    
    def _identify_strengths(self, grades_analysis: Dict) -> List[str]:
        """Identify student's academic strengths"""
        strengths = []
        grade_trends = grades_analysis.get("grade_trends", {})
        
        for subject, data in grade_trends.items():
            if data.get("average", 0) >= 4.5:  # Assuming 5-point scale
                strengths.append(subject)
            elif data.get("trend") == "improving":
                strengths.append(f"{subject} (improving)")
        
        return strengths if strengths else ["Consistent effort"]
    
    def _identify_improvements(
        self, 
        grades_analysis: Dict, 
        attendance_analysis: Dict, 
        homework_analysis: Dict
    ) -> List[str]:
        """Identify areas needing improvement"""
        improvements = []
        
        # Check grades
        grade_trends = grades_analysis.get("grade_trends", {})
        for subject, data in grade_trends.items():
            if data.get("trend") == "declining":
                improvements.append(f"{subject} grades")
            elif data.get("average", 0) < 3.0:
                improvements.append(f"{subject} performance")
        
        # Check attendance
        attendance_rate = attendance_analysis.get("attendance_stats", {}).get("attendance_rate", 100)
        if attendance_rate < 90:
            improvements.append("Attendance")
        
        # Check homework
        overdue = homework_analysis.get("homework_stats", {}).get("overdue_count", 0)
        if overdue > 2:
            improvements.append("Homework completion")
        
        return improvements if improvements else ["Continue current approach"]
