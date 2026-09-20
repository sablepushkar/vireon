from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Mapping


class EventType(StrEnum):
    LAB_RESULT = "lab_result"
    VITAL = "vital"
    TREATMENT = "treatment"
    ADVERSE_EVENT = "adverse_event"
    TRIAL_OPERATION = "trial_operation"


@dataclass(frozen=True, slots=True)
class PharmaEvent:
    event_id: str
    patient_id: str | None
    site_id: str
    event_type: EventType
    timestamp: datetime
    values: Mapping[str, float | str | bool]
    source: str

    def as_dict(self) -> dict[str, object]:
        return {
            "event_id": self.event_id,
            "patient_id": self.patient_id,
            "site_id": self.site_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "values": dict(self.values),
            "source": self.source,
        }


@dataclass(frozen=True, slots=True)
class Signal:
    signal_id: str
    event_id: str
    signal_type: str
    severity: str
    reason: str
    detected_at: datetime

    def as_dict(self) -> dict[str, object]:
        return {
            "signal_id": self.signal_id,
            "event_id": self.event_id,
            "signal_type": self.signal_type,
            "severity": self.severity,
            "reason": self.reason,
            "detected_at": self.detected_at.isoformat(),
        }
