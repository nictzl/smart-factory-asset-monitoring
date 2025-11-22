from confluent_kafka import Consumer
from core.config import settings

def get_kafka_consumer():
    return Consumer({
        "bootstrap.servers": settings.KAFKA_BOOTSTRAP,
        "group.id": settings.KAFKA_GROUP_ID,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False
    })
