from pydantic import BaseModel, Field
from datetime import datetime

class IngestPayload(BaseModel):
    machine_id: str = Field(..., example="M001")
    timestamp: datetime
    vibration: float
    temperature: float
