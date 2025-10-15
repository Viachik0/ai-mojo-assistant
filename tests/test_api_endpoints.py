import pytest
from httpx import AsyncClient
from app.main import app
import os

# Set database URL to in-memory SQLite for testing
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"


@pytest.mark.asyncio
async def test_create_user():
    """Test creating a user"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/users/",
            json={"name": "Test User", "email": "test@example.com", "role": "student"}
        )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["role"] == "student"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_users():
    """Test listing users"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/users/")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert "total" in data
    assert "page" in data
    assert "per_page" in data


@pytest.mark.asyncio
async def test_get_user():
    """Test getting a specific user"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First create a user
        create_response = await ac.post(
            "/api/users/",
            json={"name": "Test User 2", "email": "test2@example.com", "role": "teacher"}
        )
        user_id = create_response.json()["id"]
        
        # Now get the user
        response = await ac.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "Test User 2"


@pytest.mark.asyncio
async def test_analytics_summary():
    """Test analytics summary endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/analytics/reports/summary")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "timestamp" in data
    assert "total_users" in data["summary"]
    assert "total_students" in data["summary"]
    assert "total_teachers" in data["summary"]
