from fastapi import APIRouter
from app.api.master.router import router as master_router
from app.api.minio.router import router as minio_router
from app.api.user.router import router as user_router
import app.api.master.master  # noqa: F401
import app.api.user.user  # noqa: F401
import app.api.minio.minio  # noqa: F401

api_router = APIRouter()
api_router.include_router(master_router, prefix="/master", tags=["master"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(minio_router, prefix="/minio", tags=["minio"])
