from datetime import datetime, timezone
import unittest

from vireon.core.models import EventType, PharmaEvent
from vireon.signal_engine import detect_signals


class ReproducibleSignalTests(unittest.TestCase):
    def make_event(self):
        return PharmaEvent(
            event_id="EV-REPLAY-001",
            patient_id=None,
            site_id="SITE-DEMO",
            event_type=EventType.LAB_RESULT,
            timestamp=datetime(2026, 10, 1, tzinfo=timezone.utc),
            values={"biomarker_x": 140, "heart_rate": 125},
            source="synthetic-replay-test",
        )

    def test_fixed_evaluation_time_reproduces_complete_signal_objects(self):
        evaluated_at = datetime(2026, 10, 10, 12, 0, tzinfo=timezone.utc)
        event = self.make_event()
        first = detect_signals([event], evaluated_at=evaluated_at)
        second = detect_signals([event], evaluated_at=evaluated_at)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 2)
        self.assertTrue(all(signal.detected_at == evaluated_at for signal in first))

    def test_naive_evaluation_timestamp_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            detect_signals([], evaluated_at=datetime(2026, 10, 10, 12, 0))

    def test_default_timestamp_remains_timezone_aware(self):
        signals = detect_signals([self.make_event()])
        self.assertTrue(signals)
        self.assertIsNotNone(signals[0].detected_at.utcoffset())


if __name__ == "__main__":
    unittest.main()
