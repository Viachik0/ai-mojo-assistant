from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSession as AsyncSessionFactory
from app.services.database_service import DatabaseService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    """
    async with AsyncSessionFactory() as session:
        yield session


async def get_database_service(session: AsyncSession = None) -> DatabaseService:
    """
    Dependency that provides a database service instance.
    """
    if session is None:
        async with AsyncSessionFactory() as session:
            yield DatabaseService(session)
    else:
        yield DatabaseService(session)
