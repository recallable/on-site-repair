from redis.asyncio import Redis
from app.core.config import settings

redis_client = Redis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)


async def ping():
    return await redis_client.ping()


async def close():
    await redis_client.close()
