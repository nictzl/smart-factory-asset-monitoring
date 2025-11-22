Alternative (Docker — reproducible environment)
```powershell
cd services\processing-service
docker build -t sfam-process:dev .
docker run --rm -p 7999:7999 --name sfam-process sfam-process:dev
# follow logs
docker logs -f sfam-process
```

Quick tests
- Health endpoint (GET):
```powershell
Invoke-RestMethod -Method GET "http://localhost:7999/healthz"
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
