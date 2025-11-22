# Ingestion Service — Local Development

Purpose: accepts ingestion events and writes to MinIO and Kafka.

Prerequisites
- Python 3.12 (for local venv) or Docker
- `requirements.txt` contains `fastapi` and `uvicorn` and other deps

Run locally (recommended for development)

PowerShell:
```powershell
cd services\ingestion-service
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run with autoreload. `--app-dir src` makes `src` the import root so
# imports like `from api.router import ...` work.
uvicorn main:app --app-dir src --reload --host 0.0.0.0 --port 8000
```

Alternative (Docker — reproducible environment)
```powershell
cd services\ingestion-service
docker build -t sfam-ingestion:dev .
docker run --rm --env-file .env -p 8000:8000 --name sfam-ingestion sfam-ingestion:dev
# follow logs
docker logs -f sfam-ingestion
```

Quick tests
- Health endpoint (GET):
```powershell
Invoke-RestMethod -Method GET "http://localhost:8000/healthz"
```
- Ingest endpoint (POST):
```powershell
Invoke-RestMethod -Method POST "http://localhost:8000/ingest" `
  -ContentType "application/json" `
  -Body '{
    "machine_id": "M001",
    "timestamp": "2025-10-12T14:20:00Z",
    "vibration": 0.45,
    "temperature": 37.2
  }'
```

Debugging tips
- If you see `ModuleNotFoundError: No module named 'api'` when running locally, use the `--app-dir src` invocation above or run from the project root with `uvicorn src.main:app`.
- If container exits or POST returns 5xx, check `docker logs sfam-ingestion` for the stack trace.
- The service depends on MinIO and Kafka; in dev you can run them via `infra/docker-compose-dev/docker-compose.yml`.

Notes
- The `Dockerfile` runs Uvicorn with `--app-dir src` so the container imports match the code layout.
- Keep `requirements.txt` up to date; if you add packages, rebuild the image for Docker runs.
uvicorn main:app --app-dir src --reload
