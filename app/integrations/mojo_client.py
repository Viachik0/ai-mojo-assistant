import aiohttp
import logging
from typing import List, Dict, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class MojoClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.session = None

    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=self.headers)
        return self.session

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    async def get_teachers(self) -> List[Dict]:
        """Get list of teachers"""
        try:
            session = await self._get_session()
            async with session.get(f"{self.base_url}/api/teachers") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("teachers", [])
                else:
                    logger.error(f"Failed to get teachers: {response.status} - {await response.text()}")
                    return []
        except Exception as e:
            logger.error(f"Error getting teachers: {e}")
            return []
    
    async def get_students(self, class_id: Optional[str] = None) -> List[Dict]:
        """Get list of students"""
        try:
            session = await self._get_session()
            url = f"{self.base_url}/api/students"
            if class_id:
                url += f"?class_id={class_id}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("students", [])
                else:
                    logger.error(f"Failed to get students: {response.status} - {await response.text()}")
                    return []
        except Exception as e:
            logger.error(f"Error getting students: {e}")
            return []
    
    async def get_grades(self, teacher_id: str, days: int = 7) -> List[Dict]:
        """Get grades for the last N days"""
        try:
            session = await self._get_session()
            url = f"{self.base_url}/api/grades?teacher_id={teacher_id}&days={days}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("grades", [])
                else:
                    logger.error(f"Failed to get grades: {response.status} - {await response.text()}")
                    return []
        except Exception as e:
            logger.error(f"Error getting grades: {e}")
            return []
    
    async def get_missing_grades(self, teacher_id: str) -> List[Dict]:
        """Get lessons without grades"""
        try:
            session = await self._get_session()
            url = f"{self.base_url}/api/missing-grades?teacher_id={teacher_id}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("missing_grades", [])
                else:
                    logger.error(f"Failed to get missing grades: {response.status} - {await response.text()}")
                    return []
        except Exception as e:
            logger.error(f"Error getting missing grades: {e}")
            return []
    
    async def send_message(self, recipient_id: str, message: str, message_type: str = "notification") -> bool:
        """Send message through Mojo"""
        try:
            session = await self._get_session()
            payload = {
                "recipient_id": recipient_id,
                "message": message,
                "type": message_type
            }
            async with session.post(f"{self.base_url}/api/messages", json=payload) as response:
                if response.status in [200, 201]:
                    logger.info(f"Message sent to {recipient_id}: {message}")
                    return True
                else:
                    logger.error(f"Failed to send message: {response.status} - {await response.text()}")
                    return False
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    async def send_teacher_alert(self, teacher_id: str, alert_data: Dict) -> bool:
        """Send notification to teacher"""
        message = f"🔔 System Notification:\n{alert_data.get('message', '')}"
        return await self.send_message(teacher_id, message)
    
    async def send_parent_report(self, student_id: str, report_data: Dict) -> bool:
        """Send report to parent"""
        message = f"📊 Performance Report:\n{report_data.get('message', '')}"
        return await self.send_message(student_id, message, "report")