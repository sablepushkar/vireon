from __future__ import annotations
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class TrialEvent:
    event_id: str
    site_id: str
    timestamp: datetime
    event_type: str
    complete: bool = True
    protocol_deviation: bool = False

@dataclass(frozen=True, slots=True)
class SiteIntegrityResult:
    site_id: str
    status: str
    anomaly_score: float
    metrics: dict[str, float]
    flags: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)

def assess_site(site_id: str, events: list[TrialEvent]) -> SiteIntegrityResult:
    if not site_id.strip():
        raise ValueError("site_id must not be empty")
    if not events:
        raise ValueError("events must be non-empty")
    missing_rate = sum(not e.complete for e in events) / len(events)
    deviation_rate = sum(e.protocol_deviation for e in events) / len(events)
    duplicate_rate = (len(events) - len({e.timestamp for e in events})) / len(events)
    type_count = len(Counter(e.event_type for e in events))
    score = min(1.0, 0.50 * missing_rate + 0.35 * deviation_rate + 0.15 * duplicate_rate)
    flags: list[str] = []
    if missing_rate >= 0.10:
        flags.append("missing_data_pattern")
    if deviation_rate >= 0.10:
        flags.append("protocol_deviation_pattern")
    if duplicate_rate >= 0.20:
        flags.append("timestamp_collision_pattern")
    return SiteIntegrityResult(site_id, "review" if flags else "monitor", score, {
        "event_count": float(len(events)), "missing_rate": missing_rate,
        "protocol_deviation_rate": deviation_rate, "timestamp_collision_rate": duplicate_rate,
        "distinct_event_types": float(type_count),
    }, tuple(flags))
