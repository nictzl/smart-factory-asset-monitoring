from core.kafka import get_kafka_consumer
from core.config import settings
from .handler import process_event
import json
import logging
import time

consumer = get_kafka_consumer()

def start_worker():
    logging.info("Starting processing worker...")
    consumer.subscribe([settings.KAFKA_TOPIC_RAW])

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logging.error(f"Kafka error: {msg.error()}")
            continue

        try:
            event = json.loads(msg.value().decode())
            process_event(event)
            consumer.commit(msg)
        except Exception as e:
            logging.exception("Error processing message")
            time.sleep(1)
