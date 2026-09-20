from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

from .core.models import EventType, PharmaEvent
from .core.validation import EventValidationError, validate_event
from .signal_engine import detect_signals
from .storage.sqlite import EventStore


class EventRequest(BaseModel):
    event_id: str = Field(min_length=1)
    patient_id: str | None = None
    site_id: str = Field(min_length=1)
    event_type: EventType
    timestamp: datetime
    values: dict[str, float | str | bool]
    source: str = Field(min_length=1)


def _to_domain(request: EventRequest) -> PharmaEvent:
    event = PharmaEvent(
        event_id=request.event_id,
        patient_id=request.patient_id,
        site_id=request.site_id,
        event_type=request.event_type,
        timestamp=request.timestamp,
        values=request.values,
        source=request.source,
    )
    try:
        validate_event(event)
    except EventValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    return event


def create_app(database_path: str | Path = "vireon.db") -> FastAPI:
    app = FastAPI(
        title="VIREON",
        version="0.2.0",
        description="Pharmaceutical lifecycle intelligence prototype API.",
    )
    store = EventStore(database_path)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "vireon"}

    @app.post("/v1/events", status_code=status.HTTP_201_CREATED)
    def create_event(request: EventRequest) -> dict[str, Any]:
        event = _to_domain(request)
        store.save(event)
        return event.as_dict()

    @app.get("/v1/events")
    def list_events(
        limit: int = Query(default=100, ge=1, le=1000),
    ) -> dict[str, Any]:
        events = store.list_events(limit)
        return {"count": len(events), "events": [event.as_dict() for event in events]}

    @app.get("/v1/events/{event_id}")
    def get_event(event_id: str) -> dict[str, Any]:
        event = store.get(event_id)
        if event is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="event not found")
        return event.as_dict()

    @app.post("/v1/signals/detect")
    def detect_current_signals(
        limit: int = Query(default=1000, ge=1, le=1000),
    ) -> dict[str, Any]:
        events = store.list_events(limit)
        signals = detect_signals(events)
        return {"event_count": len(events), "signal_count": len(signals), "signals": [s.as_dict() for s in signals]}

    return app


app = create_app()
