from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

from .core.models import EventType, EvidenceLink, PharmaEvent
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
        version="0.3.0",
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
            raise HTTPException(status_code=404, detail="event not found")
        return event.as_dict()

    @app.post("/v1/signals/detect")
    def detect_current_signals(
        limit: int = Query(default=1000, ge=1, le=1000),
    ) -> dict[str, Any]:
        events = store.list_events(limit)
        signals = detect_signals(events)

        for signal in signals:
            store.save_evidence(
                EvidenceLink(
                    evidence_id=f"EVD-{signal.signal_id}",
                    signal_id=signal.signal_id,
                    event_id=signal.event_id,
                    relationship="detected_from",
                    detector_version=signal.detector_version,
                    created_at=signal.detected_at,
                )
            )

        return {
            "event_count": len(events),
            "signal_count": len(signals),
            "signals": [signal.as_dict() for signal in signals],
        }

    @app.get("/v1/signals/{signal_id}/evidence")
    def get_signal_evidence(signal_id: str) -> dict[str, Any]:
        evidence = store.list_evidence(signal_id)
        if not evidence:
            raise HTTPException(status_code=404, detail="evidence not found")

        links = []
        for item in evidence:
            event = store.get(item.event_id)
            links.append(
                {
                    "evidence": item.as_dict(),
                    "source_event": None if event is None else event.as_dict(),
                }
            )

        return {"signal_id": signal_id, "links": links}

    return app


app = create_app()
