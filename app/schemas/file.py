from fastapi.temp_pydantic_v1_params import Query
from pydantic import BaseModel



class FileUploadDTO(BaseModel):
    module: int = Query(..., gt=0, description="模块ID")


class FileVO(BaseModel):
    id: int = Query(..., gt=0, description="文件ID")
    bucket: str = Query(..., description="存储桶名称")
    file_name: str = Query(..., description="文件名")
    file_path: str = Query(..., description="文件路径")
