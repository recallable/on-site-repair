from sqlalchemy import BigInteger, String, Boolean, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class File(Base):
    __tablename__ = "files"
    __table_args__ = {"schema": "on_site_repair"}

    uploader_id: Mapped[int] = mapped_column(BigInteger, nullable=False,comment="上传用户ID")
    module: Mapped[int] = mapped_column(BigInteger, nullable=False,comment="模块ID")
    source_file_name: Mapped[str] = mapped_column(String(255), nullable=False,comment="源文件名")
    source_file_size: Mapped[int] = mapped_column(BigInteger, nullable=False,comment="源文件大小")
    source_file_type: Mapped[str] = mapped_column(String(255), nullable=False,comment="源文件类型")
    file_name: Mapped[str] = mapped_column(String(255), nullable=False,comment="文件名")
    file_path: Mapped[str] = mapped_column(String(255), nullable=False,comment="文件路径")
