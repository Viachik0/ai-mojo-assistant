import pytest
from unittest.mock import AsyncMock, patch
import httpx
from app.services.mojo_service import MojoService


@pytest.mark.asyncio
async def test_mojo_service_initialization():
    """Test that MojoService can be initialized with httpx.AsyncClient"""
    async with httpx.AsyncClient() as client:
        service = MojoService(client)
        assert service is not None
        assert service.client is not None
        assert service.base_url is not None
        assert service.api_token is not None


@pytest.mark.asyncio
async def test_send_message_success():
    """Test successful message sending"""
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = "OK"
    
    async with httpx.AsyncClient() as client:
        with patch.object(client, 'post', return_value=mock_response) as mock_post:
            service = MojoService(client)
            result = await service.send_message(user_id=123, text="Test message")
            
            assert result is True
            mock_post.assert_called_once()
            
            # Verify the call was made with correct parameters
            call_args = mock_post.call_args
            assert "/messages" in str(call_args)
            assert call_args.kwargs["json"]["user_id"] == 123
            assert call_args.kwargs["json"]["text"] == "Test message"
            assert "Authorization" in call_args.kwargs["headers"]


@pytest.mark.asyncio
async def test_send_message_failure():
    """Test message sending failure"""
    mock_response = AsyncMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    
    async with httpx.AsyncClient() as client:
        with patch.object(client, 'post', return_value=mock_response):
            service = MojoService(client)
            result = await service.send_message(user_id=123, text="Test message")
            
            assert result is False


@pytest.mark.asyncio
async def test_send_message_exception():
    """Test message sending with exception"""
    async with httpx.AsyncClient() as client:
        with patch.object(client, 'post', side_effect=Exception("Network error")):
            service = MojoService(client)
            result = await service.send_message(user_id=123, text="Test message")
            
            assert result is False


@pytest.mark.asyncio
async def test_get_students_stub():
    """Test that get_students returns empty list (stub)"""
    async with httpx.AsyncClient() as client:
        service = MojoService(client)
        result = await service.get_students()
        
        assert result == []


@pytest.mark.asyncio
async def test_get_students_with_class_id_stub():
    """Test that get_students with class_id returns empty list (stub)"""
    async with httpx.AsyncClient() as client:
        service = MojoService(client)
        result = await service.get_students(class_id=5)
        
        assert result == []


@pytest.mark.asyncio
async def test_get_grades_stub():
    """Test that get_grades returns empty list (stub)"""
    async with httpx.AsyncClient() as client:
        service = MojoService(client)
        result = await service.get_grades()
        
        assert result == []


@pytest.mark.asyncio
async def test_get_attendance_stub():
    """Test that get_attendance returns empty list (stub)"""
    async with httpx.AsyncClient() as client:
        service = MojoService(client)
        result = await service.get_attendance()
        
        assert result == []


@pytest.mark.asyncio
async def test_get_homework_stub():
    """Test that get_homework returns empty list (stub)"""
    async with httpx.AsyncClient() as client:
        service = MojoService(client)
        result = await service.get_homework()
        
        assert result == []


@pytest.mark.asyncio
async def test_get_lessons_stub():
    """Test that get_lessons returns empty list (stub)"""
    async with httpx.AsyncClient() as client:
        service = MojoService(client)
        result = await service.get_lessons()
        
        assert result == []
