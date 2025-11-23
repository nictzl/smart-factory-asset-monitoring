from fastapi import FastAPI
from core.logging import init_logging
from api.v1.metrics import router as metrics_router

init_logging("query-service")

app = FastAPI(title="Query Service")

app.include_router(metrics_router, prefix="/v1")

@app.get("/health")
def health():
    return {"status": "ok"}
