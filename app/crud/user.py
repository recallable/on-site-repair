import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class CRUDUser:
    """
    用户CRUD操作
    """
    async def get_by_username(self, db: AsyncSession,
                              username: str
                              ) -> Optional[User]:
        """
        根据用户名获取用户
        :param db: 数据库会话
        :param username: 用户名
        :return: User 对象
        """
        result = await db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def get_by_phone(self, db: AsyncSession,
                           phone: str
                           ) -> Optional[User]:
        """
        根据手机号获取用户
        :param db: 数据库会话
        :param phone: 手机号
        :return: User 对象
        """
        result = await db.execute(select(User).where(User.phone == phone))
        return result.scalars().first()

    async def create_by_phone(self, db: AsyncSession,
                              *,
                              phone: str,
                              username: str = '匿名用户',
                              password: str = '123456'
                              ) -> User:
        """
        根据手机号创建用户
        :param db: 数据库会话
        :param phone: 手机号
        :param username: 用户名 (默认: 匿名用户)
        :param password: 密码 (默认: 123456)
        :return: User 对象
        """
        user = User(phone=phone, username=username, password=password,last_login_time=datetime.datetime.now())
        db.add(user)
        await db.commit()
        return user


user_crud = CRUDUser()
