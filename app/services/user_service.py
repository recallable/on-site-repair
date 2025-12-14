import random
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.redis import redis_client
from app.services.strategy.user_login_strategy import LoginStrategyFactory
from app.utils.jwt_utils import JWTUtil
from app.utils.sms_utils import SmsUtil


class UserService:
    async def login(self, db: AsyncSession, login_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        统一登录接口
        """
        # 1. 获取策略并执行登录
        strategy = LoginStrategyFactory.get_strategy(login_type)
        user = await strategy.login(db, data)

        # 2. 提取用户信息用于生成 Token
        # user 可能是 ORM 对象或字典
        if hasattr(user, "id"):
            user_id = str(user.id)
            username = user.username
        else:
            user_id = str(user.get("id"))
            username = user.get("username")

        # 3. 生成 Token
        # scope 可以根据业务逻辑设置，这里默认为 user
        token = JWTUtil.create_token({"sub": user_id, "scope": "user", "username": username})

        return {
            "token": token,
            "message": "登录成功",
            "userInfo": {
                "id": user_id,
                "username": username
            }
        }

    async def send_sms(self, phone: str):
        """
        发送短信
        """
        code = str(random.randint(1000, 9999))
        await redis_client.setex(f"user:login:sms:{phone}", 60 * 50000000000, code)
        await SmsUtil.send_sms(phone, code)
        return code


user_service = UserService()
