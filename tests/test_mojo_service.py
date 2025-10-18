"""
Tests for MojoService - Mojo.education integration
"""
import pytest
import httpx
from app.services.mojo_service import MojoService


@pytest.mark.asyncio
async def test_send_message_success():
    """Test successful message sending"""
    
    def mock_handler(request: httpx.Request) -> httpx.Response:
        """Mock HTTP handler that returns success"""
        # Verify request method and path
        assert request.method == "POST"
        assert request.url.path == "/api/messaging/message"
        
        # Verify authorization header
        assert "Authorization" in request.headers
        assert request.headers["Authorization"] == "Bearer test_token"
        
        # Verify request payload
        import json
        payload = json.loads(request.content)
        assert "userIds" in payload
        assert "title" in payload
        assert "text" in payload
        assert payload["userIds"] == [123, 456]
        assert payload["title"] == "Test Title"
        assert payload["text"] == "Test message content"
        
        # Return success response
        return httpx.Response(200, json={"status": "ok"})
    
    # Create mock transport and client
    mock_transport = httpx.MockTransport(mock_handler)
    async with httpx.AsyncClient(
        transport=mock_transport,
        base_url="https://test.mojo.education",
        headers={"Authorization": "Bearer test_token"}
    ) as client:
        service = MojoService(client)
        
        # Test with multiple user IDs
        result = await service.send_message(
            user_ids=[123, 456],
            text="Test message content",
            title="Test Title"
        )
        
        assert result is True


@pytest.mark.asyncio
async def test_send_message_success_single_user():
    """Test successful message sending with single user ID"""
    
    def mock_handler(request: httpx.Request) -> httpx.Response:
        """Mock HTTP handler that returns success"""
        import json
        payload = json.loads(request.content)
        
        # Verify single user ID is converted to list
        assert payload["userIds"] == [789]
        assert payload["title"] == "AI-Ассистент"  # Default title
        
        return httpx.Response(200, json={"status": "ok"})
    
    mock_transport = httpx.MockTransport(mock_handler)
    async with httpx.AsyncClient(
        transport=mock_transport,
        base_url="https://test.mojo.education",
        headers={"Authorization": "Bearer test_token"}
    ) as client:
        service = MojoService(client)
        
        # Test with single user ID (int)
        result = await service.send_message(
            user_ids=789,
            text="Single user message"
        )
        
        assert result is True


@pytest.mark.asyncio
async def test_send_message_failure_http_error():
    """Test message sending failure with HTTP error (401 Unauthorized)"""
    
    def mock_handler(request: httpx.Request) -> httpx.Response:
        """Mock HTTP handler that returns 401 error"""
        return httpx.Response(
            401, 
            json={"error": "Unauthorized", "message": "Invalid token"}
        )
    
    mock_transport = httpx.MockTransport(mock_handler)
    async with httpx.AsyncClient(
        transport=mock_transport,
        base_url="https://test.mojo.education",
        headers={"Authorization": "Bearer invalid_token"}
    ) as client:
        service = MojoService(client)
        
        result = await service.send_message(
            user_ids=[123],
            text="Test message",
            title="Test"
        )
        
        # Should return False on HTTP error
        assert result is False


@pytest.mark.asyncio
async def test_send_message_failure_server_error():
    """Test message sending failure with server error (500)"""
    
    def mock_handler(request: httpx.Request) -> httpx.Response:
        """Mock HTTP handler that returns 500 error"""
        return httpx.Response(500, json={"error": "Internal Server Error"})
    
    mock_transport = httpx.MockTransport(mock_handler)
    async with httpx.AsyncClient(
        transport=mock_transport,
        base_url="https://test.mojo.education",
        headers={"Authorization": "Bearer test_token"}
    ) as client:
        service = MojoService(client)
        
        result = await service.send_message(
            user_ids=[123],
            text="Test message",
            title="Test"
        )
        
        assert result is False


@pytest.mark.asyncio
async def test_stub_methods_raise_not_implemented():
    """Test that stub methods raise NotImplementedError"""
    
    # Create a minimal mock client (won't be used by stub methods)
    mock_transport = httpx.MockTransport(lambda r: httpx.Response(200))
    async with httpx.AsyncClient(
        transport=mock_transport,
        base_url="https://test.mojo.education"
    ) as client:
        service = MojoService(client)
        
        # Test all stub methods
        with pytest.raises(NotImplementedError, match="get_students"):
            await service.get_students()
        
        with pytest.raises(NotImplementedError, match="get_teachers"):
            await service.get_teachers()
        
        with pytest.raises(NotImplementedError, match="get_subjects"):
            await service.get_subjects()
        
        with pytest.raises(NotImplementedError, match="get_grades"):
            await service.get_grades()
        
        with pytest.raises(NotImplementedError, match="get_attendance"):
            await service.get_attendance()
        
        with pytest.raises(NotImplementedError, match="get_homework"):
            await service.get_homework()
