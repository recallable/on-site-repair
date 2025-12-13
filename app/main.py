from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes import api_router
from app.api.ws.chat import register_ws
from app.db.session import engine, get_session
from app.middleware.exception import register_exception_middleware
from app.middleware.logging import register_access_log_middleware
from app.services.minio_service import minio_client, ensure_bucket, get_file_preview_by_id
from app.services.redis import redis_client, close as redis_close


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await redis_client.ping()
    except Exception:
        pass
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        pass
    # try:
    #     # await init_db(engine)
    # except Exception:
    #     pass
    try:
        ensure_bucket()
    except Exception:
        pass
    yield
    try:
        await redis_close()
    except Exception:
        pass
    try:
        await engine.dispose()
    except Exception:
        pass


app = FastAPI(lifespan=lifespan)
register_exception_middleware(app)
register_access_log_middleware(app)
register_ws(app)
app.include_router(api_router, prefix="/api")


@app.get("/health")
async def health():
    r = False
    db = False
    m = False
    try:
        r = await redis_client.ping()
    except Exception:
        r = False
    try:
        from sqlalchemy import text
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            db = True
    except Exception:
        db = False
    try:
        from app.core.config import settings
        m = minio_client.bucket_exists(settings.minio_bucket)
    except Exception:
        m = False
    return {"redis": bool(r), "postgres": bool(db), "minio": bool(m)}
