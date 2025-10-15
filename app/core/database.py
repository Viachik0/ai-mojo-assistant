import sqlalchemy.ext.asyncio as sa_asyncio
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Base model
Base = declarative_base()

# Async engine setup
engine = sa_asyncio.create_async_engine(settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"), echo=True)

# Async session setup
AsyncSession = sessionmaker(engine, class_=sa_asyncio.AsyncSession, expire_on_commit=False)