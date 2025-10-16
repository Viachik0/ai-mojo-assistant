import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- ГЛАВНОЕ ИСПРАВЛЕНИЕ ---
# Добавляем корень проекта в sys.path ДО импорта любых модулей приложения.
# Это гарантирует, что Python найдет пакет 'app'.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -------------------------

from app.main import app
from app.core.database import Base, get_db

# Используем SQLite в файле для тестирования
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """
    Зависимость, которая предоставляет тестовую сессию БД и закрывает ее после.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Переопределяем зависимость get_db на нашу тестовую функцию
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    """
    Фикстура, которая предоставляет тестовый клиент API.
    Создает и удаляет таблицы БД для каждого теста для полной изоляции.
    """
    # Удаляем старую БД, если она есть
    if os.path.exists("./test.db"):
        os.remove("./test.db")
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")
