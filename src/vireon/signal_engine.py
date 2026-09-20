from __future__ import annotations

from datetime import datetime, timezone

from .core.models import PharmaEvent, Signal
from .core.validation import validate_event


DETECTOR_VERSION = "threshold-rules/0.2"


def detect_signals(events: list[PharmaEvent]) -> list[Signal]:
    """Apply deterministic, versioned VIREON rules to validated events."""
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
                    reason=(
                        "biomarker_x is at or above the VIREON 0.2 "
                        "demonstration threshold of 130"
                    ),
                    detector_version=DETECTOR_VERSION,
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
                    reason=(
                        "heart_rate is at or above the VIREON 0.2 "
                        "demonstration threshold of 120"
                    ),
                    detector_version=DETECTOR_VERSION,
                    detected_at=datetime.now(timezone.utc),
                )

        if signal is not None:
            signals.append(signal)

    return signals
