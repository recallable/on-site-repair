from minio import Minio
import io
import os
import uuid
from app.core.config import settings

minio_client = Minio(
    settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_secure,
)


def ensure_bucket():
    exists = minio_client.bucket_exists(settings.minio_bucket)
    if not exists:
        minio_client.make_bucket(settings.minio_bucket)


def _gen_object_name(filename: str, prefix: str = "") -> str:
    ext = os.path.splitext(filename)[1] or ""
    name = f"{uuid.uuid4().hex}{ext}"
    if prefix:
        return f"{prefix.strip('/').rstrip('/')}/{name}"
    return name


def upload_data(filename: str, data: bytes, prefix: str = "", bucket: str | None = None, content_type: str | None = None) -> dict:
    ensure_bucket()
    bkt = bucket or settings.minio_bucket
    object_name = _gen_object_name(filename, prefix)
    minio_client.put_object(bkt, object_name, io.BytesIO(data), length=len(data), content_type=content_type)
    return {"bucket": bkt, "object_name": object_name}
