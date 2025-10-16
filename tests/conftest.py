import os
import sys
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# --- ГЛАВНОЕ ИСПРАВЛЕНИЕ ---
# Добавляем корень проекта в sys.path ДО импорта любых модулей приложения.
# Это гарантирует, что Python найдет пакет 'app'.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -------------------------

from app.main import app
from app.core.database import Base
from app.core.database import get_db as core_get_db
from app.api.dependencies import get_db as api_get_db

# Используем SQLite в файле для тестирования
TEST_DB_FILE = "./test.db"
SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DB_FILE}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=False, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def override_get_db():
    """
    Зависимость, которая предоставляет тестовую сессию БД и закрывает ее после.
    """
    async with TestingSessionLocal() as session:
        yield session

# Переопределяем обе зависимости get_db на нашу тестовую функцию
app.dependency_overrides[core_get_db] = override_get_db
app.dependency_overrides[api_get_db] = override_get_db


@pytest.fixture(scope="function")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """
    Автоматическая фикстура для настройки БД перед каждым тестом.
    """
    # Remove old database if exists
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Cleanup
    await engine.dispose()
    
    # Remove database file
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)


@pytest.fixture(scope="function")
def client():
    """
    Фикстура, которая предоставляет тестовый клиент API.
    """
    with TestClient(app) as c:
        yield c
