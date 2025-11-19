from confluent_kafka import Producer
from .config import settings

def get_kafka_producer():
    return Producer({
        "bootstrap.servers": settings.KAFKA_BOOTSTRAP,
        "enable.idempotence": True,           # industry standard
        "linger.ms": 5,                       # small batching
        "acks": "all",
        "compression.type": "lz4"
    })
