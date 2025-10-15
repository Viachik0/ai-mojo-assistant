import redis.asyncio as redis
from src.core.config import settings

redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True
)


async def get_redis_client() -> redis.Redis:
    """
    Returns an async Redis client from the connection pool.
    """
    return redis.Redis(connection_pool=redis_pool)