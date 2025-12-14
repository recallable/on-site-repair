from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.user.router import router
from app.schemas.user import LoginDTO
from app.services.user_service import user_service
from app.db.session import get_session
from app.utils.response import APIResponse

@router.post('/login')
async def login(dto: LoginDTO, db: AsyncSession = Depends(get_session)):
    """
    用户登录
    支持：账号密码、微信、钉钉、QQ
    """
    result = await user_service.login(db, dto.login_type.value, dto.model_dump())
    return APIResponse.success(data=result)
