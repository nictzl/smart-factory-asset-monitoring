from minio import Minio
from minio.error import S3Error
import logging
import io
from core.config import settings


_minio_client = None


def get_minio_client() -> Minio:
    """
    Returns a singleton MinIO client instance.
    This ensures the connection is reused efficiently.
    """
    global _minio_client

    if _minio_client is None:
        logging.info("Initializing MinIO client...")

        _minio_client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )

    return _minio_client


def upload_file(bucket: str, object_name: str, data: bytes, content_type: str = "application/octet-stream"):
    """
    Upload bytes data to MinIO.
    """
    client = get_minio_client()

    try:
        # MinIO client expects a file-like object with a read() method.
        buf = io.BytesIO(data)
        client.put_object(
            bucket_name=bucket,
            object_name=object_name,
            data=buf,
            length=len(data),
            content_type=content_type,
        )
        logging.info(f"Uploaded to MinIO: bucket={bucket}, object={object_name}")

    except S3Error as e:
        logging.error(f"MinIO upload failed: {e}")
        raise e
