from typing import Optional

from fastapi import UploadFile, File, Query

from app.api.minio.router import router
from app.services.minio_service import upload_data


@router.post("/upload")
async def upload(file: UploadFile = File(...), prefix: str = Query(default=""), bucket: Optional[str] = None):
    data = await file.read()
    res = upload_data(filename=file.filename or "file", data=data, prefix=prefix or "", bucket=bucket,
                      content_type=file.content_type)
    return res
