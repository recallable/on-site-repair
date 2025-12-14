from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "on-site-repair"
    redis_url: str = "redis://localhost:6379/0"
    postgres_dsn: str = "postgresql+asyncpg://postgres:121518@localhost:5432/postgres"
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_secure: bool = False
    minio_bucket: str = "default"
    secret_key: str = "your-secret-key-here"  # JWT 密钥，生产环境请修改
    algorithm: str = "HS256"                  # JWT 算法
    access_token_expire_minutes: int = 30     # Token 过期时间
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
