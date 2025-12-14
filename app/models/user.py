import datetime

from sqlalchemy import BigInteger, String, SMALLINT, TIMESTAMP, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    """
    CREATE TABLE IF NOT EXISTS user_info
    (
        id              BIGSERIAL PRIMARY KEY,
        username        VARCHAR(20),
        phone           VARCHAR(20),
        password        VARCHAR(100),
        nickname        VARCHAR(50),
        avatar_id       BIGINT,
        gender          SMALLINT  DEFAULT 0,
        user_status     SMALLINT  DEFAULT 1,
        last_login_time TIMESTAMP,
        is_deleted      BOOLEAN   DEFAULT FALSE,
        created_time    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        update_time     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    COMMENT ON TABLE user_info IS '用户信息表';
    COMMENT ON COLUMN user_info.id IS '主键ID';
    COMMENT ON COLUMN user_info.username IS '用户账号';
    COMMENT ON COLUMN user_info.phone IS '用户手机号（登录账号）';
    COMMENT ON COLUMN user_info.password IS '加密后的登录密码（MD5/BCrypt）';
    COMMENT ON COLUMN user_info.nickname IS '用户昵称';
    COMMENT ON COLUMN user_info.avatar_id IS '用户头像ID（单文件，关联files.id）';
    COMMENT ON COLUMN user_info.gender IS '用户性别（0-未知 1-男 2-女）';
    COMMENT ON COLUMN user_info.user_status IS '用户状态（0-禁用 1-正常）';
    COMMENT ON COLUMN user_info.last_login_time IS '最后登录时间';
    COMMENT ON COLUMN user_info.is_deleted IS '是否删除（true-已删除 false-未删除）';
    COMMENT ON COLUMN user_info.created_time IS '创建时间';
    COMMENT ON COLUMN user_info.update_time IS '更新时间（自动更新）';
    """
    __tablename__ = "user_info"
    __table_args__ = {"schema": "on_site_repair"}

    username: Mapped[str] = mapped_column(String(20),comment="用户账号")
    phone: Mapped[str] = mapped_column(String(20),comment="用户手机号（登录账号）")
    password: Mapped[str] = mapped_column(String(100),comment="加密后的登录密码（MD5/BCrypt）")
    nickname: Mapped[str] = mapped_column(String(50),comment="用户昵称")
    avatar_id: Mapped[int] = mapped_column(BigInteger,comment="用户头像ID（单文件，关联files.id）")
    gender: Mapped[int] = mapped_column(SMALLINT, default=0,comment="用户性别（0-未知 1-男 2-女）")
    user_status: Mapped[int] = mapped_column(SMALLINT, default=1,comment="用户状态（0-禁用 1-正常）")
    last_login_time: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=True,comment="最后登录时间")
