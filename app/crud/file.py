from sqlalchemy.ext.asyncio import AsyncSession

from app.models.file import File as FileEntity


async def create_file(
        session: AsyncSession,
        *,
        uploader_id: int,
        module: int,
        source_file_name: str,
        source_file_size: int,
        source_file_type: str,
        file_name: str,
        file_path: str,
) -> FileEntity:
    """
    创建文件实体

    :param session: 数据库会话
    :param uploader_id: 上传者ID
    :param module: 模块ID
    :param source_file_name: 源文件名
    :param source_file_size: 源文件大小
    :param source_file_type: 源文件类型
    :param file_name: 文件名
    :param file_path: 文件路径
    :return: 创建的文件实体
    """

    entity = FileEntity(
        uploader_id=uploader_id,
        module=module,
        source_file_name=source_file_name,
        source_file_size=source_file_size,
        source_file_type=source_file_type,
        file_name=file_name,
        file_path=file_path,
        is_deleted=False,
    )
    session.add(entity)
    await session.commit()
    await session.refresh(entity)
    return entity
