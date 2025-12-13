from fastapi import APIRouter

from app.utils.response import APIResponse

router = APIRouter()


@router.get("/ping")
async def ping():
    return APIResponse.success({"ok": True, "scope": "master"})