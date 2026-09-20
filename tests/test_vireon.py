from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone

from vireon.core.models import EventType, PharmaEvent
from vireon.core.validation import EventValidationError, validate_event
from vireon.signal_engine import detect_signals


class VireonTests(unittest.TestCase):
    def _event(
        self,
        *,
        event_type: EventType = EventType.LAB_RESULT,
        values: dict[str, float | str | bool] | None = None,
    ) -> PharmaEvent:
        return PharmaEvent(
            event_id="E-001",
            patient_id="P-001",
            site_id="S-01",
            event_type=event_type,
            timestamp=datetime.now(timezone.utc) - timedelta(minutes=1),
            values=values or {"biomarker_x": 135.0},
            source="test",
        )

    def test_future_timestamp_is_rejected(self) -> None:
        event = PharmaEvent(
            event_id="E-001",
            patient_id="P-001",
            site_id="S-01",
            event_type=EventType.VITAL,
            timestamp=datetime.now(timezone.utc) + timedelta(minutes=5),
            values={"heart_rate": 70},
            source="test",
        )
        with self.assertRaises(EventValidationError):
            validate_event(event)

    def test_missing_lab_values_are_rejected(self) -> None:
        event = self._event(values={})
        with self.assertRaises(EventValidationError):
            validate_event(event)

    def test_signal_contains_detector_version(self) -> None:
        signals = detect_signals([self._event()])
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].detector_version, "threshold-rules/0.2")

    def test_normal_event_has_no_signal(self) -> None:
        event = self._event(values={"biomarker_x": 90.0})
        self.assertEqual(detect_signals([event]), [])


if __name__ == "__main__":
    unittest.main()
