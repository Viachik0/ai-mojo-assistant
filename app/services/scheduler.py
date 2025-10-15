import asyncio
import schedule
import logging
from typing import Optional
from app.integrations.mojo_client import MojoClient
from app.services.analysis_service import AnalysisService

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self, mojo_client: MojoClient):
        self.mojo_client = mojo_client
        self.analysis_service = AnalysisService(mojo_client)
        self.is_running = False
        self.task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the scheduler"""
        self.is_running = True
        self.task = asyncio.create_task(self._run_scheduler())
        logger.info("Scheduler started")
    
    async def stop(self):
        """Stop the scheduler"""
        self.is_running = False
        if self.task:
            self.task.cancel()
        logger.info("Scheduler stopped")
    
    async def _run_scheduler(self):
        """Main scheduler loop"""
        # Schedule tasks
        schedule.every(10).minutes.do(self._check_grading_timeliness)
        schedule.every().monday.at("09:00").do(self._send_weekly_reports)
        schedule.every().day.at("08:00").do(self._check_attendance_alerts)
        schedule.every().day.at("18:00").do(self._check_homework_alerts)
        
        while self.is_running:
            try:
                schedule.run_pending()
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(60)
    
    async def _check_grading_timeliness(self):
        """Check for missing grades"""
        logger.info("Checking grading timeliness...")
        try:
            await self.analysis_service.check_missing_grades()
        except Exception as e:
            logger.error(f"Error in grading check: {e}")
    
    async def _send_weekly_reports(self):
        """Send weekly reports to parents"""
        logger.info("Sending weekly reports...")
        try:
            await self.analysis_service.generate_weekly_reports()
        except Exception as e:
            logger.error(f"Error sending weekly reports: {e}")
    
    async def _check_attendance_alerts(self):
        """Check for attendance issues and send alerts"""
        logger.info("Checking attendance patterns...")
        try:
            students = await self.mojo_client.get_students()
            
            for student in students:
                # Analyze last 7 days of attendance
                attendance_analysis = await self.analysis_service.analyze_student_attendance(
                    student['id'], 
                    days=7
                )
                
                # Send alerts if any issues detected
                alerts = attendance_analysis.get("alerts", [])
                for alert in alerts:
                    if alert:
                        await self.mojo_client.send_message(
                            student['id'], 
                            f"⚠️ Attendance Alert:\n{alert}",
                            "alert"
                        )
        except Exception as e:
            logger.error(f"Error checking attendance alerts: {e}")
    
    async def _check_homework_alerts(self):
        """Check for homework completion issues and send alerts"""
        logger.info("Checking homework completion...")
        try:
            students = await self.mojo_client.get_students()
            
            for student in students:
                # Analyze homework completion
                homework_analysis = await self.analysis_service.analyze_homework_completion(
                    student['id'], 
                    days=7
                )
                
                # Send alerts if any overdue homework
                alerts = homework_analysis.get("alerts", [])
                for alert in alerts:
                    if alert:
                        await self.mojo_client.send_message(
                            student['id'], 
                            f"📚 Homework Alert:\n{alert}",
                            "alert"
                        )
        except Exception as e:
            logger.error(f"Error checking homework alerts: {e}")