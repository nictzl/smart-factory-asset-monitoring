from fastapi import APIRouter, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from .schemas import IngestPayload
from core.kafka import get_kafka_producer
from storage.minio_client import get_minio_client
from core.config import settings
import json
import uuid
import logging
import io
import time

router = APIRouter()
logger = logging.getLogger("ingestion.api")
producer = get_kafka_producer()
minio = get_minio_client()


@router.post("/ingest")
async def ingest(payload: IngestPayload, request: Request):
    trace_id = str(uuid.uuid4())

    # Use FastAPI's jsonable_encoder to convert datetime -> ISO strings and other types
    event = jsonable_encoder(payload)
    event["ingested_at"] = payload.timestamp.isoformat()
    event["trace_id"] = trace_id

    # Serialize once
    serialized = json.dumps(event)
    serialized_bytes = serialized.encode()

    minio_ok = False
    kafka_ok = False

    # 1. Write to MinIO (length must be bytes length). MinIO expects a file-like object.
    try:
        buf = io.BytesIO(serialized_bytes)
        minio.put_object(
            bucket_name=settings.MINIO_BUCKET_RAW,
            object_name=f"{payload.machine_id}/{trace_id}.json",
            data=buf,
            length=len(serialized_bytes),
            content_type="application/json",
        )
        minio_ok = True
    except Exception as e:
        logger.exception("Failed to write object to MinIO: %s", e)

    # 2. Publish to Kafka (handle connection failures with simple retries)
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            producer.produce(
                settings.KAFKA_TOPIC_RAW,
                value=serialized_bytes,
            )
            producer.flush()
            kafka_ok = True
            break
        except Exception as e:
            logger.exception("Attempt %d: Failed to publish to Kafka: %s", attempt, e)
            time.sleep(0.5)

    # If both MinIO and Kafka failed, return 503 so the caller can retry
    if not minio_ok and not kafka_ok:
        logger.error("Both MinIO and Kafka persistence failed for trace_id=%s", trace_id)
        raise HTTPException(status_code=503, detail="Failed to persist event")

    return {"status": "ok", "trace_id": trace_id, "minio": minio_ok, "kafka": kafka_ok}
