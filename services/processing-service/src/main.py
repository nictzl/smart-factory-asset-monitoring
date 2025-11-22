from fastapi import FastAPI
from core.logging import init_logging
from consumer.worker import start_worker
import threading

app = FastAPI()
init_logging()

@app.on_event("startup")
def startup_event():
    t = threading.Thread(target=start_worker)
    t.daemon = True
    t.start()

@app.get("/healthz")
def health():
    return {"status": "ok"}
