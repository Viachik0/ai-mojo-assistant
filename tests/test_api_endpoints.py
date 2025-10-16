import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import engine, Base
import os

# Set database URL to PostgreSQL for testing
os.environ["DATABASE_URL"] = "postgresql+asyncpg://postgres:password@localhost:5432/mojo_assistant_test"


@pytest.fixture(scope="function")
async def setup_database():
    """Setup database before each test"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_user(setup_database):
    """Test creating a user"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/users/",
            json={"name": "Test User", "email": "test@example.com", "role": "student"}
        )
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["role"] == "student"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_users(setup_database):
    """Test listing users"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/users/")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert "total" in data
    assert "page" in data
    assert "per_page" in data


@pytest.mark.asyncio
async def test_get_user(setup_database):
    """Test getting a specific user"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # First create a user
        create_response = await ac.post(
            "/api/users/",
            json={"name": "Test User 2", "email": "test2@example.com", "role": "teacher"}
        )
        assert create_response.status_code == 201
        user_id = create_response.json()["id"]
        
        # Now get the user
        response = await ac.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "Test User 2"


@pytest.mark.asyncio
async def test_analytics_summary(setup_database):
    """Test analytics summary endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/analytics/reports/summary")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "timestamp" in data
    assert "total_users" in data["summary"]
    assert "total_students" in data["summary"]
    assert "total_teachers" in data["summary"]

