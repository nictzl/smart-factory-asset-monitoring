import redis.asyncio as redis
from core.config import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db
)

async def get(key: str):
    return await redis_client.get(key)

async def set(key: str, value: str):
    await redis_client.set(key, value, ex=settings.cache_ttl_seconds)
