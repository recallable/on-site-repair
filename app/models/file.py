from sqlalchemy import BigInteger, String, Boolean, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class File(Base):
    __tablename__ = "files"
    __table_args__ = {"schema": "on_site_repair"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uploader_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    module: Mapped[int] = mapped_column(BigInteger, nullable=False)
    source_file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    source_file_type: Mapped[str] = mapped_column(String(255), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    created_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("now()"))
    updated_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("now()"))
