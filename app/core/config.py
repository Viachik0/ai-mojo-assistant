import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Mojo API Configuration
    MOJO_BASE_URL = os.getenv("MOJO_BASE_URL", "https://mojo.education/api")
    MOJO_API_KEY = os.getenv("MOJO_API_KEY", "")
    
    # Mojo.education API Configuration
    MOJO_API_BASE_URL = os.getenv("MOJO_API_BASE_URL", "https://koriphey.mojo.education/public")
    MOJO_API_TOKEN = os.getenv("MOJO_API_TOKEN", "")
    
    # AI Configuration (vLLM)
    VLLM_API_BASE = os.getenv("VLLM_API_BASE", "http://localhost:8001/v1")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "deepseek-chat")
    
    # Application Settings
    CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "60"))
    GRADING_DEADLINE_DAYS = int(os.getenv("GRADING_DEADLINE_DAYS", "3"))
    WEEKLY_REPORT_DAY = os.getenv("WEEKLY_REPORT_DAY", "monday")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/mojo_assistant")
    
    # Convert postgresql:// to postgresql+asyncpg:// for async support
    if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    # Security
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")

settings = Settings()