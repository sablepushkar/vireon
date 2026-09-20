from __future__ import annotations

from datetime import datetime, timezone

from .core.models import PharmaEvent, Signal
from .core.validation import validate_event


def detect_signals(events: list[PharmaEvent]) -> list[Signal]:
    """Apply deterministic V0.1 rules to validated events."""
    signals: list[Signal] = []

    for event in events:
        validate_event(event)
        signal: Signal | None = None

        if event.event_type.value == "lab_result":
            biomarker = event.values.get("biomarker_x")
            if isinstance(biomarker, (int, float)) and biomarker >= 130:
                signal = Signal(
                    signal_id=f"SIG-{event.event_id}",
                    event_id=event.event_id,
                    signal_type="biomarker_elevation",
                    severity="moderate",
                    reason="biomarker_x is at or above the V0.1 threshold of 130",
                    detected_at=datetime.now(timezone.utc),
                )

        elif event.event_type.value == "vital":
            heart_rate = event.values.get("heart_rate")
            if isinstance(heart_rate, (int, float)) and heart_rate >= 120:
                signal = Signal(
                    signal_id=f"SIG-{event.event_id}",
                    event_id=event.event_id,
                    signal_type="elevated_heart_rate",
                    severity="moderate",
                    reason="heart_rate is at or above the V0.1 threshold of 120",
                    detected_at=datetime.now(timezone.utc),
                )

        if signal is not None:
            signals.append(signal)

    return signals
