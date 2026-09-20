from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Any
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from .ai_guard import ModelSpec, assess_model
from .core.models import EventType, EvidenceLink, PharmaEvent
from .core.validation import EventValidationError, validate_event
from .digital_measures import validate_digital_measure
from .evidence_graph import EvidenceGraph
from .lifecycle import simulate_lifecycle
from .signal_engine import detect_signals
from .storage.sqlite import EventStore
from .trial_integrity import TrialEvent, assess_site

class EventRequest(BaseModel):
    event_id: str = Field(min_length=1)
    patient_id: str | None = None
    site_id: str = Field(min_length=1)
    event_type: EventType
    timestamp: datetime
    values: dict[str, float | str | bool]
    source: str = Field(min_length=1)

class ModelGuardRequest(BaseModel):
    model_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    context_of_use: str = Field(min_length=1)
    risk_tier: str = Field(min_length=1)
    validation_status: str = Field(min_length=1)
    reference: list[float] = Field(min_length=1)
    current: list[float] = Field(min_length=1)
    missing_reference: float = 0.0
    missing_current: float = 0.0

class DigitalMeasureRequest(BaseModel):
    measure_id: str = Field(min_length=1)
    values: list[float | None] = Field(min_length=1)
    expected_min: float | None = None
    expected_max: float | None = None

class TrialEventRequest(BaseModel):
    event_id: str
    site_id: str
    timestamp: datetime
    event_type: str
    complete: bool = True
    protocol_deviation: bool = False

def _to_domain(request: EventRequest) -> PharmaEvent:
    event = PharmaEvent(request.event_id, request.patient_id, request.site_id, request.event_type, request.timestamp, request.values, request.source)
    try:
        validate_event(event)
    except EventValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return event

def create_app(database_path: str | Path = "vireon.db") -> FastAPI:
    app = FastAPI(title="VIREON", version="1.0.0", description="Synthetic-data-first pharmaceutical lifecycle intelligence prototype.")
    store = EventStore(database_path)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "vireon", "version": "1.0.0"}

    @app.post("/v1/events", status_code=status.HTTP_201_CREATED)
    def create_event(request: EventRequest) -> dict[str, Any]:
        event = _to_domain(request); store.save(event); return event.as_dict()

    @app.get("/v1/events")
    def list_events(limit: int = Query(default=100, ge=1, le=1000)) -> dict[str, Any]:
        events = store.list_events(limit); return {"count": len(events), "events": [e.as_dict() for e in events]}

    @app.get("/v1/events/{event_id}")
    def get_event(event_id: str) -> dict[str, Any]:
        event = store.get(event_id)
        if event is None: raise HTTPException(status_code=404, detail="event not found")
        return event.as_dict()

    @app.post("/v1/signals/detect")
    def detect_current_signals(limit: int = Query(default=1000, ge=1, le=1000)) -> dict[str, Any]:
        events = store.list_events(limit); signals = detect_signals(events)
        for signal in signals:
            store.save_evidence(EvidenceLink(f"EVD-{signal.signal_id}", signal.signal_id, signal.event_id, "detected_from", signal.detector_version, signal.detected_at))
        return {"event_count": len(events), "signal_count": len(signals), "signals": [s.as_dict() for s in signals]}

    @app.get("/v1/signals/{signal_id}/evidence")
    def get_signal_evidence(signal_id: str) -> dict[str, Any]:
        evidence = store.list_evidence(signal_id)
        if not evidence: raise HTTPException(status_code=404, detail="evidence not found")
        links = []
        for x in evidence:
            event = store.get(x.event_id)
            links.append({"evidence": x.as_dict(), "source_event": None if event is None else event.as_dict()})
        return {"signal_id": signal_id, "links": links}

    @app.get("/v1/evidence/graph")
    def evidence_graph(limit: int = Query(default=1000, ge=1, le=1000)) -> dict[str, object]:
        graph = EvidenceGraph(); events = store.list_events(limit); signals = detect_signals(events)
        for event in events: graph.add_event(event)
        for signal in signals:
            graph.add_signal(signal)
            graph.add_evidence(EvidenceLink(f"EVD-{signal.signal_id}", signal.signal_id, signal.event_id, "detected_from", signal.detector_version, signal.detected_at))
        return graph.as_dict()

    @app.post("/v1/ai-guard/assess")
    def ai_guard(request: ModelGuardRequest) -> dict[str, object]:
        result = assess_model(ModelSpec(request.model_id, request.version, request.context_of_use, request.risk_tier, request.validation_status), request.reference, request.current, missing_reference=request.missing_reference, missing_current=request.missing_current)
        return {"model": request.model_dump(exclude={"reference","current","missing_reference","missing_current"}), "assessment": {"status": result.status, "risk_flags": result.risk_flags, "metrics": result.metrics}}

    @app.post("/v1/digital-measures/validate")
    def digital_measure(request: DigitalMeasureRequest) -> dict[str, object]:
        return validate_digital_measure(request.measure_id, request.values, expected_min=request.expected_min, expected_max=request.expected_max).as_dict()

    @app.post("/v1/trial-integrity/sites/{site_id}/assess")
    def trial_integrity(site_id: str, events: list[TrialEventRequest]) -> dict[str, object]:
        if not events: raise HTTPException(status_code=422, detail="events must be non-empty")
        domain = [TrialEvent(e.event_id, e.site_id, e.timestamp, e.event_type, e.complete, e.protocol_deviation) for e in events]
        return assess_site(site_id, domain).as_dict()

    @app.get("/v1/lifecycle/{candidate_id}")
    def lifecycle(candidate_id: str) -> dict[str, object]:
        return {"candidate_id": candidate_id, "snapshots": [s.as_dict() for s in simulate_lifecycle(candidate_id)], "safety_boundary": "workflow simulation only; no clinical or regulatory decision is produced"}

    return app

app = create_app()
