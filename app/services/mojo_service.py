"""
Mojo.education Service - Integration with Mojo.education messaging API
"""
import logging
from typing import Union, Iterable, List
from contextlib import asynccontextmanager
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


class MojoService:
    """Service for interacting with Mojo.education API"""
    
    def __init__(self, client: httpx.AsyncClient):
        """
        Initialize MojoService with an httpx AsyncClient
        
        Args:
            client: Configured httpx.AsyncClient instance
        """
        self.client = client
    
    async def send_message(
        self, 
        user_ids: Union[int, Iterable[int]], 
        text: str, 
        title: str = "AI-Ассистент"
    ) -> bool:
        """
        Send message to users via Mojo.education messaging API
        
        Args:
            user_ids: Single user ID or iterable of user IDs
            text: Message text content
            title: Message title (default: "AI-Ассистент")
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        # Convert single user_id to list
        if isinstance(user_ids, int):
            user_ids_list = [user_ids]
        else:
            user_ids_list = list(user_ids)
        
        # Prepare request payload
        payload = {
            "userIds": user_ids_list,
            "title": title,
            "text": text
        }
        
        try:
            response = await self.client.post(
                "/api/messaging/message",
                json=payload
            )
            
            if response.status_code == 200:
                logger.info(f"Message sent successfully to {len(user_ids_list)} user(s): {title}")
                return True
            else:
                logger.error(
                    f"Failed to send message. Status: {response.status_code}, "
                    f"Response: {response.text}"
                )
                return False
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred while sending message: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error occurred while sending message: {e}")
            return False
    
    async def get_students(self) -> List:
        """
        Get list of students (not yet implemented)
        
        Raises:
            NotImplementedError: This method is a stub
        """
        raise NotImplementedError("get_students method not yet implemented")
    
    async def get_teachers(self) -> List:
        """
        Get list of teachers (not yet implemented)
        
        Raises:
            NotImplementedError: This method is a stub
        """
        raise NotImplementedError("get_teachers method not yet implemented")
    
    async def get_subjects(self) -> List:
        """
        Get list of subjects (not yet implemented)
        
        Raises:
            NotImplementedError: This method is a stub
        """
        raise NotImplementedError("get_subjects method not yet implemented")
    
    async def get_grades(self) -> List:
        """
        Get grades data (not yet implemented)
        
        Raises:
            NotImplementedError: This method is a stub
        """
        raise NotImplementedError("get_grades method not yet implemented")
    
    async def get_attendance(self) -> List:
        """
        Get attendance data (not yet implemented)
        
        Raises:
            NotImplementedError: This method is a stub
        """
        raise NotImplementedError("get_attendance method not yet implemented")
    
    async def get_homework(self) -> List:
        """
        Get homework data (not yet implemented)
        
        Raises:
            NotImplementedError: This method is a stub
        """
        raise NotImplementedError("get_homework method not yet implemented")


# Global instance
_mojo_service: MojoService | None = None


@asynccontextmanager
async def mojo_service_lifespan():
    """
    Context manager for MojoService lifecycle management
    
    Yields:
        MojoService: Configured MojoService instance
    """
    global _mojo_service
    
    # Create httpx client with base_url and Authorization header
    client = httpx.AsyncClient(
        base_url=settings.MOJO_API_BASE_URL,
        headers={"Authorization": f"Bearer {settings.MOJO_API_TOKEN}"},
        timeout=30.0
    )
    
    try:
        _mojo_service = MojoService(client)
        logger.info("MojoService initialized successfully")
        yield _mojo_service
    finally:
        await client.aclose()
        _mojo_service = None
        logger.info("MojoService closed successfully")


async def get_mojo_service() -> MojoService:
    """
    Dependency for getting MojoService instance
    
    Returns:
        MojoService: The global MojoService instance
        
    Raises:
        RuntimeError: If MojoService is not initialized
    """
    if _mojo_service is None:
        raise RuntimeError(
            "MojoService is not initialized. "
            "Use mojo_service_lifespan context manager to initialize it."
        )
    return _mojo_service
