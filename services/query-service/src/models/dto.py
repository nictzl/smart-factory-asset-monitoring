from pydantic import BaseModel
from typing import List


class Metric(BaseModel):
    timestamp: str
    rms: float
    temperature: float


class MetricsResponse(BaseModel):
    machine_id: str
    data: List[Metric]
