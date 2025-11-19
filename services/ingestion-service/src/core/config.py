from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "ingestion-service"
    ENV: str = "dev"

    # Default for compose environment where Kafka service is named `kafka`.
    # This value can be overridden via `.env` (e.g. for local dev use `localhost:9092`).
    KAFKA_BOOTSTRAP: str = "kafka:29092"
    KAFKA_TOPIC_RAW: str = "sensor.raw"

    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_RAW: str = "raw"

    class Config:
        env_file = ".env"

settings = Settings()

