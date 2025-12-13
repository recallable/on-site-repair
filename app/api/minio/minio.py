import os

from fastapi import UploadFile, File as UploadFileParam, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import filetype
from app.api.minio.router import router
from app.db.session import get_session
from app.schemas.file import FileUploadDTO
from app.services.minio_service import upload_file_and_record
from app.utils.response import APIResponse


@router.post("/upload")
async def upload(
        file: UploadFile = UploadFileParam(...),
        dto: FileUploadDTO = Depends(),
        session: AsyncSession = Depends(get_session),
):
    """
    上传文件
    :param file: 上传的文件
    :param dto: 文件上传DTO
    :param session: 数据库会话
    :return: 文件VO
    """
    data = await file.read()
    if file.size != len(data):
        raise HTTPException(status_code=400, detail="提供的文件大小与实际大小不匹配")

    # 文件真实类型校验
    kind = filetype.guess(data)
    if kind is None:
        raise HTTPException(status_code=400, detail="无法识别文件类型")

    # 检查扩展名是否匹配
    ext = os.path.splitext(file.filename)[1].lower().strip('.')
    if ext != kind.extension:
        # 特殊处理：jpeg 和 jpg 视为相同
        if not (ext in ['jpg', 'jpeg'] and kind.extension in ['jpg', 'jpeg']):
            raise HTTPException(status_code=400,
                                detail=f"文件扩展名与实际类型不匹配: 预期 {kind.extension}, 实际 {ext}")

    file_type = file.filename.split('.')[-1]
    vo = await upload_file_and_record(session, dto, file_type, file.size, file.filename, data)
    return APIResponse.success(vo)
