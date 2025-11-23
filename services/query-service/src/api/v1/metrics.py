from fastapi import APIRouter, Depends, Query
from core.redis_cache import get, set
from core.database import get_db_connection
from models.dto import Metric, MetricsResponse
import json

router = APIRouter()


@router.get("/metrics/{machine_id}", response_model=MetricsResponse)
async def get_metrics(
    machine_id: str,
    limit: int = Query(100, ge=1, le=500),
):
    cache_key = f"metrics:{machine_id}:{limit}"

    # ---- 1. Check cache ----
    cached = await get(cache_key)
    if cached:
        return json.loads(cached)

    # ---- 2. Fallback to database ----
    conn = await get_db_connection()
    cur = conn.cursor()

    await cur.execute(
        """
        SELECT timestamp, vibration_rms, temperature
        FROM machine_metrics
        WHERE machine_id = %s
        ORDER BY timestamp DESC
        LIMIT %s;
        """,
        (machine_id, limit)
    )

    rows = await cur.fetchall()
    await cur.close()
    await conn.close()

    data = [
        Metric(timestamp=str(r[0]), rms=r[1], temperature=r[2]).dict()
        for r in rows
    ]

    response = MetricsResponse(
        machine_id=machine_id,
        data=data
    ).dict()

    # ---- 3. Store in cache ----
    await set(cache_key, json.dumps(response))

    return response
