# app/routers/telemetry.py
from fastapi import APIRouter
from pydantic import BaseModel
from prometheus_client import Counter

router = APIRouter(prefix="/telemetry", tags=["telemetry"])

MOBILE_EVENTS = Counter(
    "mobile_events_total", "Eventos móviles reportados por la app", ["type"]
)

class TelemetryEvent(BaseModel):
    type: str   # ej: 'ticket_closed' | 'location_sent' | 'api_error'
    meta: dict | None = None

@router.post("/")
def push_event(evt: TelemetryEvent):
    MOBILE_EVENTS.labels(evt.type).inc()
    # Si quieres, aquí puedes guardar evt.meta en DB o logs
    return {"ok": True}
