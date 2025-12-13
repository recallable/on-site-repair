from sqlalchemy.ext.asyncio import AsyncEngine
from app.models.base import Base


async def init_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
