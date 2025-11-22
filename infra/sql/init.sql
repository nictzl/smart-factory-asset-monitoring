CREATE TABLE IF NOT EXISTS machine_metrics (
    id SERIAL PRIMARY KEY,
    machine_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    vibration REAL,
    vibration_rms REAL,
    temperature REAL,
    temp_moving_avg REAL,
    anomaly_score REAL,
    processed_at TIMESTAMP NOT NULL DEFAULT NOW()
);
