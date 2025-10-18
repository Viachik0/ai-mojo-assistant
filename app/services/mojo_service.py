import httpx
import logging
from typing import Union, Iterable, List, Dict, Optional
from contextlib import asynccontextmanager
from app.core.config import settings

logger = logging.getLogger(__name__)

# Module-level client instance
_mojo_client: Optional[httpx.AsyncClient] = None


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
    
    async def send_message(
        self, 
        user_ids: Union[int, Iterable[int]], 
        text: str, 
        title: str = "AI-Ассистент"
    ) -> bool:
        """
        Send a message to one or multiple users through Mojo API
        
        Args:
            user_ids: The ID(s) of the user(s) to send the message to (single int or iterable)
            text: The message text to send
            title: The message title (default: "AI-Ассистент")
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        try:
            # Normalize user_ids to a list
            if isinstance(user_ids, int):
                user_ids_list = [user_ids]
            else:
                user_ids_list = list(user_ids)
            
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "userIds": user_ids_list,
                "title": title,
                "text": text
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/messaging/message",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            
            logger.info(f"Message sent successfully to users {user_ids_list}")
            return True
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error sending message: {e.response.status_code} - {e.response.text}")
            return False
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    async def get_students(self, class_id: Optional[int] = None) -> List[Dict]:
        """
        Get list of students from Mojo API
        
        Args:
            class_id: Optional class ID to filter students
            
        Returns:
            List of student dictionaries
        """
        raise NotImplementedError("get_students is not yet implemented")
    
    async def get_teachers(self) -> List[Dict]:
        """
        Get list of teachers from Mojo API
        
        Returns:
            List of teacher dictionaries
        """
        raise NotImplementedError("get_teachers is not yet implemented")
    
    async def get_subjects(self) -> List[Dict]:
        """
        Get list of subjects from Mojo API
        
        Returns:
            List of subject dictionaries
        """
        raise NotImplementedError("get_subjects is not yet implemented")
    
    async def get_grades(self, student_id: Optional[int] = None, days: Optional[int] = None) -> List[Dict]:
        """
        Get grades from Mojo API
        
        Args:
            student_id: Optional student ID to filter grades
            days: Optional number of days to look back
            
        Returns:
            List of grade dictionaries
        """
        raise NotImplementedError("get_grades is not yet implemented")
    
    async def get_attendance(self, student_id: Optional[int] = None, days: Optional[int] = None) -> List[Dict]:
        """
        Get attendance records from Mojo API
        
        Args:
            student_id: Optional student ID to filter attendance
            days: Optional number of days to look back
            
        Returns:
            List of attendance dictionaries
        """
        raise NotImplementedError("get_attendance is not yet implemented")
    
    async def get_homework(self, student_id: Optional[int] = None) -> List[Dict]:
        """
        Get homework assignments from Mojo API
        
        Args:
            student_id: Optional student ID to filter homework
            
        Returns:
            List of homework dictionaries
        """
        raise NotImplementedError("get_homework is not yet implemented")


@asynccontextmanager
async def mojo_service_lifespan():
    """
    Context manager for MojoService lifecycle management.
    Creates and manages the httpx.AsyncClient for the service.
    """
    global _mojo_client
    
    _mojo_client = httpx.AsyncClient(
        base_url=settings.MOJO_API_BASE_URL,
        headers={"Authorization": f"Bearer {settings.MOJO_API_TOKEN}"}
    )
    
    try:
        yield
    finally:
        if _mojo_client:
            await _mojo_client.aclose()
            _mojo_client = None


async def get_mojo_service() -> MojoService:
    """
    FastAPI dependency for getting MojoService instance.
    
    Returns:
        MojoService: Configured service instance
    
    Raises:
        RuntimeError: If called outside of lifespan context
    """
    if _mojo_client is None:
        raise RuntimeError("MojoService client not initialized. Use mojo_service_lifespan context manager.")
    
    return MojoService(_mojo_client)
