from __future__ import annotations

from datetime import datetime, timezone
from math import isfinite
from typing import Iterable

from .core.models import PharmaEvent, Signal
from .core.validation import validate_event

DETECTOR_VERSION = "threshold-rules/0.2"


def _number(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    value = float(value)
    return value if isfinite(value) else None


def detect_signals(
    events: Iterable[PharmaEvent],
    *,
    biomarker_x_threshold: float = 130.0,
    heart_rate_threshold: float = 120.0,
) -> list[Signal]:
    if not isfinite(float(biomarker_x_threshold)) or not isfinite(float(heart_rate_threshold)):
        raise ValueError("signal thresholds must be finite")
    signals: list[Signal] = []
    for event in events:
        validate_event(event)
        biomarker = _number(event.values.get("biomarker_x"))
        heart_rate = _number(event.values.get("heart_rate"))

        if biomarker is not None and biomarker >= biomarker_x_threshold:
            signals.append(
                Signal(
                    signal_id=f"SIG-{event.event_id}",
                    event_id=event.event_id,
                    signal_type="biomarker_x_high",
                    severity="review",
                    reason=f"biomarker_x={biomarker:g} >= threshold={biomarker_x_threshold:g}",
                    detector_version=DETECTOR_VERSION,
                    detected_at=datetime.now(timezone.utc),
                )
            )

        if heart_rate is not None and heart_rate >= heart_rate_threshold:
            signals.append(
                Signal(
                    signal_id=f"SIG-{event.event_id}-HEART_RATE",
                    event_id=event.event_id,
                    signal_type="heart_rate_high",
                    severity="review",
                    reason=f"heart_rate={heart_rate:g} >= threshold={heart_rate_threshold:g}",
                    detector_version=DETECTOR_VERSION,
                    detected_at=datetime.now(timezone.utc),
                )
            )

    return signals
