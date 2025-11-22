import json
from analytics.metrics import compute_vibration_rms, compute_temp_moving_avg
from analytics.anomalies import compute_anomaly_score
from core.db import get_db_conn
from storage.minio_client import get_minio_client
from core.config import settings

def process_event(event: dict):
    machine_id = event["machine_id"]
    timestamp = event["timestamp"]
    vibration = event["vibration"]
    temperature = event["temperature"]

    # Ensure numeric results are native Python floats (avoid numpy types leaking into DB/JSON)
    vib_rms = float(compute_vibration_rms(vibration))
    temp_avg = float(compute_temp_moving_avg(temperature))
    anomaly = float(compute_anomaly_score(vibration))

    enriched = {
        **event,
        "vibration_rms": vib_rms,
        "temp_moving_avg": temp_avg,
        "anomaly_score": anomaly
    }

    # 1. Write to Postgres
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO machine_metrics 
        (machine_id, timestamp, vibration, vibration_rms, temperature, temp_moving_avg, anomaly_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (machine_id, timestamp, vibration, vib_rms, temperature, temp_avg, anomaly)
    )
    conn.commit()
    cur.close()
    conn.close()

    # 2. Write to MinIO
    # 2. Write to MinIO using upload helper (which wraps bytes in a file-like buffer)
    minio_client = get_minio_client()
    from storage.minio_client import upload_file

    serialized = json.dumps(enriched)
    upload_file(
        bucket=settings.MINIO_BUCKET_PROCESSED,
        object_name=f"{machine_id}/{event['trace_id']}.json",
        data=serialized.encode(),
        content_type="application/json",
    )
