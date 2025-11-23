from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_host: str = "host.docker.internal"
    postgres_port: int = 5435
    postgres_user: str = "admin"
    postgres_password: str = "admin123"
    postgres_db: str = "sfam"

    redis_host: str = "host.docker.internal"
    redis_port: int = 6379
    redis_db: int = 0

    cache_ttl_seconds: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
