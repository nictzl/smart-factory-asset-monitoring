from fastapi import FastAPI
from api.router import router
from core.logging import init_logging
from core.config import settings

app = FastAPI(title=settings.APP_NAME)
init_logging()

app.include_router(router)

@app.get("/healthz")
def health():
    return {"status": "ok"}
