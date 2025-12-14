import hashlib
from abc import ABC, abstractmethod
from typing import Dict, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import user_crud
from app.middleware.exception import BusinessException
from app.models.user import User
from app.services.redis import redis_client


class LoginStrategy(ABC):
    @abstractmethod
    async def login(self, db: AsyncSession, data: Dict[str, Any]) -> Union[User, Dict[str, Any]]:
        """
        执行登录逻辑
        :param db: 数据库会话
        :param data: 登录数据 (包含 username, password, code 等)
        :return: User 对象或用户信息字典
        """
        pass


class AccountLoginStrategy(LoginStrategy):
    """
    账号密码登录策略
    """
    async def login(self, db: AsyncSession, data: Dict[str, Any]) -> User:
        """
        账号密码登录
        :param db: 数据库会话
        :param data: 登录数据 (包含 username, password)
        :return: User 对象
        """
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            raise BusinessException(code=400, message="请输入用户名和密码")

        # 优先尝试手机号登录
        user = await user_crud.get_by_phone(db, username)
        if not user:
            # 尝试用户名登录
            user = await user_crud.get_by_username(db, username)

        if not user:
            raise BusinessException(code=404, message="用户不存在")

        password = hashlib.sha256(password.encode()).hexdigest()
        if user.password != password:
            raise BusinessException(code=401, message="密码错误")

        return user


class WeChatLoginStrategy(LoginStrategy):
    """
    微信登录策略
    """
    async def login(self, db: AsyncSession, data: Dict[str, Any]) -> User:
        """
        微信登录
        :param db: 数据库会话
        :param data: 登录数据 (包含 code)
        :return: User 对象
        """
        code = data.get("code")
        if not code:
            raise BusinessException(code=400, message="缺少微信授权码")
        # TODO: 实现微信登录逻辑
        # 1. 调用微信 API 获取 openid/unionid
        # 2. 查询数据库是否存在绑定该 openid 的用户
        # 3. 如果存在返回用户，不存在则注册或报错

        # 模拟返回
        return {"id": 999, "username": "wechat_mock", "nickname": "微信测试用户", "role": "user"}


class DingTalkLoginStrategy(LoginStrategy):
    """
    钉钉登录策略
    """
    async def login(self, db: AsyncSession, data: Dict[str, Any]) -> User:
        """
        钉钉登录
        :param db: 数据库会话
        :param data: 登录数据 (包含 code)
        :return: User 对象
        """
        code = data.get("code")
        if not code:
            raise BusinessException(code=400, message="缺少钉钉授权码")
        # TODO: 实现钉钉登录逻辑
        return {"id": 888, "username": "dingtalk_mock", "nickname": "钉钉测试用户", "role": "user"}


class QQLoginStrategy(LoginStrategy):
    """
    QQ登录策略
    """
    async def login(self, db: AsyncSession, data: Dict[str, Any]) -> User:
        """
        QQ登录
        :param db: 数据库会话
        :param data: 登录数据 (包含 code)
        :return: User 对象
        """
        code = data.get("code")
        if not code:
            raise BusinessException(code=400, message="缺少QQ授权码")
        # TODO: 实现QQ登录逻辑
        return {"id": 777, "username": "qq_mock", "nickname": "QQ测试用户", "role": "user"}


class PhoneLoginStrategy(LoginStrategy):
    """
    手机号登录策略
    """
    async def login(self, db: AsyncSession, data: Dict[str, Any]) -> User:
        """
        手机号登录
        :param db: 数据库会话
        :param data: 登录数据 (包含 username, code)
        :return: User 对象
        """
        phone = data.get("username")
        code = data.get("code")

        if not phone:
            raise BusinessException(code=400, message="请输入手机号")
        if not code:
            raise BusinessException(code=400, message="请输入验证码")

        key = f"user:login:sms:{phone}"
        if not (redis_code := await redis_client.get(key)):
            raise BusinessException(code=400, message="验证码已过期")

        if code != redis_code:
            raise BusinessException(code=400, message="验证码错误")

        # 查询用户
        user = await user_crud.get_by_phone(db, phone)
        if not user:
            password = hashlib.sha256(phone.encode()).hexdigest()
            user = await user_crud.create_by_phone(db, phone=phone,username=phone, password=password)
            await redis_client.delete(key)
        return user


class LoginStrategyFactory:
    """
    登录策略工厂
    """
    _strategies = {
        "account": AccountLoginStrategy(),
        "wechat": WeChatLoginStrategy(),
        "dingtalk": DingTalkLoginStrategy(),
        "qq": QQLoginStrategy(),
        "phone": PhoneLoginStrategy()
    }

    @classmethod
    def get_strategy(cls, login_type: str) -> LoginStrategy:
        """
        获取登录策略
        :param login_type: 登录类型
        :return: 登录策略对象
        """
        strategy = cls._strategies.get(login_type)
        if not strategy:
            raise BusinessException(code=400, message=f"不支持的登录方式: {login_type}")
        return strategy
