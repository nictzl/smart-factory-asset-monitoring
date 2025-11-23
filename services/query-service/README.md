Alternative (Docker — reproducible environment)
```powershell
cd services\query-service
docker build -t sfam-query:dev .
docker run --rm -p 8002:8002 --name sfam-query sfam-query:dev
# follow logs
docker logs -f sfam-query
```

Quick tests
- Health endpoint (GET):
```powershell
Invoke-RestMethod -Method GET "http://localhost:8002/healthz"
```
- Ingest endpoint (GET):
```powershell
Invoke-RestMethod -Method GET "http://localhost:8002/v1/metrics/M001?limit=50"
```
