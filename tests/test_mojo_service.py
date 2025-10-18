import pytest
import httpx
from app.services.mojo_service import MojoService


def mock_handler_success(request: httpx.Request) -> httpx.Response:
    """Mock handler that returns 200 OK"""
    return httpx.Response(200, json={"status": "ok"})


def mock_handler_unauthorized(request: httpx.Request) -> httpx.Response:
    """Mock handler that returns 401 Unauthorized"""
    return httpx.Response(401, json={"error": "Unauthorized"})


@pytest.mark.asyncio
async def test_mojo_service_initialization():
    """Test that MojoService can be initialized with httpx.AsyncClient"""
    transport = httpx.MockTransport(mock_handler_success)
    async with httpx.AsyncClient(transport=transport) as client:
        service = MojoService(client)
        assert service is not None
        assert service.client is not None
        assert service.base_url is not None
        assert service.api_token is not None


@pytest.mark.asyncio
async def test_send_message_success():
    """Test successful message sending with single user_id"""
    def handler(request: httpx.Request) -> httpx.Response:
        # Verify the request
        assert request.method == "POST"
        assert "/api/messaging/message" in str(request.url)
        assert "Authorization" in request.headers
        assert request.headers["Authorization"].startswith("Bearer ")
        
        # Parse and verify payload
        import json
        payload = json.loads(request.content)
        assert payload["userIds"] == [123]
        assert payload["text"] == "Test message"
        assert payload["title"] == "AI-Ассистент"
        
        return httpx.Response(200, json={"status": "ok"})
    
    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        service = MojoService(client)
        result = await service.send_message(user_ids=123, text="Test message")
        
        assert result is True


@pytest.mark.asyncio
async def test_send_message_success_multiple_users():
    """Test successful message sending with multiple user_ids"""
    def handler(request: httpx.Request) -> httpx.Response:
        # Verify the request
        assert request.method == "POST"
        assert "/api/messaging/message" in str(request.url)
        
        # Parse and verify payload
        import json
        payload = json.loads(request.content)
        assert payload["userIds"] == [123, 456, 789]
        assert payload["text"] == "Test message"
        assert payload["title"] == "Custom Title"
        
        return httpx.Response(200, json={"status": "ok"})
    
    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        service = MojoService(client)
        result = await service.send_message(
            user_ids=[123, 456, 789], 
            text="Test message",
            title="Custom Title"
        )
        
        assert result is True


@pytest.mark.asyncio
async def test_send_message_failure_http_error():
    """Test message sending failure with HTTP 401 error"""
    transport = httpx.MockTransport(mock_handler_unauthorized)
    async with httpx.AsyncClient(transport=transport) as client:
        service = MojoService(client)
        result = await service.send_message(user_ids=123, text="Test message")
        
        assert result is False


@pytest.mark.asyncio
async def test_send_message_failure_500():
    """Test message sending failure with HTTP 500 error"""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})
    
    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        service = MojoService(client)
        result = await service.send_message(user_ids=123, text="Test message")
        
        assert result is False


@pytest.mark.asyncio
async def test_send_message_exception():
    """Test message sending with network exception"""
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.NetworkError("Network error")
    
    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        service = MojoService(client)
        result = await service.send_message(user_ids=123, text="Test message")
        
        assert result is False


@pytest.mark.asyncio
async def test_get_students_not_implemented():
    """Test that get_students raises NotImplementedError"""
    transport = httpx.MockTransport(mock_handler_success)
    async with httpx.AsyncClient(transport=transport) as client:
        service = MojoService(client)
        
        with pytest.raises(NotImplementedError, match="get_students is not yet implemented"):
            await service.get_students()


@pytest.mark.asyncio
async def test_get_students_with_class_id_not_implemented():
    """Test that get_students with class_id raises NotImplementedError"""
    transport = httpx.MockTransport(mock_handler_success)
    async with httpx.AsyncClient(transport=transport) as client:
        service = MojoService(client)
        
        with pytest.raises(NotImplementedError, match="get_students is not yet implemented"):
            await service.get_students(class_id=5)


@pytest.mark.asyncio
async def test_get_teachers_not_implemented():
    """Test that get_teachers raises NotImplementedError"""
    transport = httpx.MockTransport(mock_handler_success)
    async with httpx.AsyncClient(transport=transport) as client:
        service = MojoService(client)
        
        with pytest.raises(NotImplementedError, match="get_teachers is not yet implemented"):
            await service.get_teachers()


@pytest.mark.asyncio
async def test_get_subjects_not_implemented():
    """Test that get_subjects raises NotImplementedError"""
    transport = httpx.MockTransport(mock_handler_success)
    async with httpx.AsyncClient(transport=transport) as client:
        service = MojoService(client)
        
        with pytest.raises(NotImplementedError, match="get_subjects is not yet implemented"):
            await service.get_subjects()


@pytest.mark.asyncio
async def test_get_grades_not_implemented():
    """Test that get_grades raises NotImplementedError"""
    transport = httpx.MockTransport(mock_handler_success)
    async with httpx.AsyncClient(transport=transport) as client:
        service = MojoService(client)
        
        with pytest.raises(NotImplementedError, match="get_grades is not yet implemented"):
            await service.get_grades()


@pytest.mark.asyncio
async def test_get_attendance_not_implemented():
    """Test that get_attendance raises NotImplementedError"""
    transport = httpx.MockTransport(mock_handler_success)
    async with httpx.AsyncClient(transport=transport) as client:
        service = MojoService(client)
        
        with pytest.raises(NotImplementedError, match="get_attendance is not yet implemented"):
            await service.get_attendance()


@pytest.mark.asyncio
async def test_get_homework_not_implemented():
    """Test that get_homework raises NotImplementedError"""
    transport = httpx.MockTransport(mock_handler_success)
    async with httpx.AsyncClient(transport=transport) as client:
        service = MojoService(client)
        
        with pytest.raises(NotImplementedError, match="get_homework is not yet implemented"):
            await service.get_homework()
