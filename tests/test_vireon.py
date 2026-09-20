from datetime import datetime, timezone
import unittest

from vireon.core.models import EventType, PharmaEvent
from vireon.core.validation import EventValidationError, validate_event
from vireon.signal_engine import detect_signals
from vireon.simulator import generate_events


class VireonCoreTests(unittest.TestCase):
    def test_simulator_is_deterministic(self) -> None:
        first = [event.as_dict() for event in generate_events(count=10, seed=7)]
        second = [event.as_dict() for event in generate_events(count=10, seed=7)]
        self.assertEqual(first, second)

    def test_future_event_is_rejected(self) -> None:
        event = PharmaEvent(
            event_id="E1",
            patient_id="P1",
            site_id="S1",
            event_type=EventType.VITAL,
            timestamp=datetime(2999, 1, 1, tzinfo=timezone.utc),
            values={"heart_rate": 70.0},
            source="test",
        )
        with self.assertRaises(EventValidationError):
            validate_event(event)

    def test_missing_lab_value_is_rejected(self) -> None:
        event = PharmaEvent(
            event_id="E2",
            patient_id="P1",
            site_id="S1",
            event_type=EventType.LAB_RESULT,
            timestamp=datetime.now(timezone.utc),
            values={},
            source="test",
        )
        with self.assertRaises(EventValidationError):
            validate_event(event)

    def test_signal_engine_flags_threshold_crossing(self) -> None:
        event = PharmaEvent(
            event_id="E3",
            patient_id="P1",
            site_id="S1",
            event_type=EventType.LAB_RESULT,
            timestamp=datetime.now(timezone.utc),
            values={"biomarker_x": 135.0},
            source="test",
        )
        signals = detect_signals([event])
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].signal_type, "biomarker_elevation")
        self.assertEqual(signals[0].severity, "moderate")

    def test_normal_event_produces_no_signal(self) -> None:
        event = PharmaEvent(
            event_id="E4",
            patient_id="P1",
            site_id="S1",
            event_type=EventType.VITAL,
            timestamp=datetime.now(timezone.utc),
            values={"heart_rate": 75.0},
            source="test",
        )
        self.assertEqual(detect_signals([event]), [])


if __name__ == "__main__":
    unittest.main()
