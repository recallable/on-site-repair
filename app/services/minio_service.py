import io
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.file import create_file
from app.models.file import File
from app.schemas.file import FileUploadDTO, FileVO

minio_client = Minio(
    settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_secure,
)


def ensure_bucket(bucket: str | None = None):
    """
    确保存储桶存在
    :param bucket: 存储桶名称
    """
    bkt = bucket or settings.minio_bucket
    exists = minio_client.bucket_exists(bkt)
    if not exists:
        minio_client.make_bucket(bkt)


def _gen_object_name(filename: str
                     ) -> str:
    """
    :param filename: 文件名
    :return:        生成的对象名称
    """
    ext = os.path.splitext(filename)[1] or ""
    name = f"{uuid.uuid4().hex}{ext}"
    date_path = datetime.now().strftime("%Y/%m/%d")
    return f"{date_path}/{name}"


def upload_data(filename: str,
                data: bytes,
                bucket: str | None = None,
                content_type: str | None = None
                ) -> dict:
    """
    :param filename:     文件名
    :param data:         文件数据
    :param bucket:       存储桶名称
    :param content_type: 内容类型
    :return:             包含存储桶名称和对象名称的字典
    """
    bkt = bucket or settings.minio_bucket
    ensure_bucket(bkt)
    object_name = _gen_object_name(filename)
    minio_client.put_object(bkt, object_name, io.BytesIO(data), length=len(data), content_type=content_type)
    return {"bucket": bkt, "object_name": object_name}


async def upload_file_and_record(
        session: AsyncSession,
        dto: FileUploadDTO,
        user_id: int,
        source_file_type: str,
        source_file_size: int,
        source_file_name: str,
        data: bytes
) -> FileVO:
    """
    上传文件并记录到数据库
    :param source_file_name:   源文件名
    :param source_file_type:   源文件类型
    :param source_file_size:   源文件大小
    :param session: 数据库会话
    :param dto: 文件上传DTO
    :param data: 文件数据
    :return: 文件VO
    """

    res = upload_data(
        filename=source_file_name,
        data=data,
        bucket="on-site-repair",
        content_type=source_file_type
    )
    object_name = res["object_name"]
    base_name = os.path.basename(object_name)

    entity = await create_file(
        session,
        uploader_id=user_id,
        module=dto.module,
        source_file_name=source_file_name,
        source_file_size=source_file_size,
        source_file_type=source_file_type,
        file_name=base_name,
        file_path=object_name,
    )

    return FileVO(
        id=entity.id,
        bucket=res["bucket"],
        file_name=entity.file_name,
        file_path=entity.file_path
    )


async def get_file_preview_by_id(
        session: AsyncSession,
        file_id: int
) -> Optional[str]:
    """
    根据文件ID获取文件信息
    :param session: 数据库会话
    :param file_id: 文件ID
    :return: 文件信息
    """
    entity = await session.get(File, file_id)
    print(entity)
    if entity is None:
        return None
    url = minio_client.presigned_get_object(
        bucket_name="on-site-repair",
        object_name=Optional[entity.file_path],
        expires=timedelta(minutes=30)
    )
    return url
