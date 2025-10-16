import httpx
import logging
from typing import List, Dict, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class MojoService:
    """Service for interacting with Mojo.education API"""
    
    def __init__(self, client: httpx.AsyncClient):
        """
        Initialize MojoService with an AsyncClient
        
        Args:
            client: httpx.AsyncClient instance for making HTTP requests
        """
        self.client = client
        self.base_url = settings.MOJO_API_BASE_URL
        self.api_token = settings.MOJO_API_TOKEN
    
    async def send_message(self, user_id: int, text: str) -> bool:
        """
        Send a message to a user through Mojo API
        
        Args:
            user_id: The ID of the user to send the message to
            text: The message text to send
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "user_id": user_id,
                "text": text
            }
            
            response = await self.client.post(
                f"{self.base_url}/messages",
                json=payload,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"Message sent successfully to user {user_id}")
                return True
            else:
                logger.error(f"Failed to send message: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending message to user {user_id}: {e}")
            return False
    
    async def get_students(self, class_id: Optional[int] = None) -> List[Dict]:
        """
        Get list of students from Mojo API
        
        Args:
            class_id: Optional class ID to filter students
            
        Returns:
            List of student dictionaries
        """
        # TODO: Implement when API endpoint is available
        logger.warning("get_students method is not yet implemented")
        return []
    
    async def get_grades(self, student_id: Optional[int] = None, days: Optional[int] = None) -> List[Dict]:
        """
        Get grades from Mojo API
        
        Args:
            student_id: Optional student ID to filter grades
            days: Optional number of days to look back
            
        Returns:
            List of grade dictionaries
        """
        # TODO: Implement when API endpoint is available
        logger.warning("get_grades method is not yet implemented")
        return []
    
    async def get_attendance(self, student_id: Optional[int] = None, days: Optional[int] = None) -> List[Dict]:
        """
        Get attendance records from Mojo API
        
        Args:
            student_id: Optional student ID to filter attendance
            days: Optional number of days to look back
            
        Returns:
            List of attendance dictionaries
        """
        # TODO: Implement when API endpoint is available
        logger.warning("get_attendance method is not yet implemented")
        return []
    
    async def get_homework(self, student_id: Optional[int] = None) -> List[Dict]:
        """
        Get homework assignments from Mojo API
        
        Args:
            student_id: Optional student ID to filter homework
            
        Returns:
            List of homework dictionaries
        """
        # TODO: Implement when API endpoint is available
        logger.warning("get_homework method is not yet implemented")
        return []
    
    async def get_lessons(self, class_id: Optional[int] = None) -> List[Dict]:
        """
        Get lessons from Mojo API
        
        Args:
            class_id: Optional class ID to filter lessons
            
        Returns:
            List of lesson dictionaries
        """
        # TODO: Implement when API endpoint is available
        logger.warning("get_lessons method is not yet implemented")
        return []
