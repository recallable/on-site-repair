from sqlalchemy import BigInteger, TIMESTAMP, Boolean, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True,comment="主键ID")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"),comment="是否删除")
    created_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("now()"),comment="创建时间")
    updated_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("now()"),comment="更新时间")


