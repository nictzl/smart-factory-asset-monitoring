from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "processing-service"
    ENV: str = "dev"

    KAFKA_BOOTSTRAP: str = "host.docker.internal:9092"
    KAFKA_TOPIC_RAW: str = "sensor.raw"
    KAFKA_GROUP_ID: str = "processing-service-group"

    POSTGRES_HOST: str = "host.docker.internal"
    POSTGRES_PORT: int = 5435
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin123"
    POSTGRES_DB: str = "sfam"

    MINIO_ENDPOINT: str = "host.docker.internal:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_PROCESSED: str = "processed"
    MINIO_SECURE: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
