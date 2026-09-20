from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from vireon.core.models import EventType, PharmaEvent
from vireon.storage.sqlite import EventStore


class StorageTests(unittest.TestCase):
    def test_event_survives_store_recreation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "nested" / "vireon.db"
            original = PharmaEvent(
                event_id="E-PERSIST-001",
                patient_id="P-001",
                site_id="S-01",
                event_type=EventType.VITAL,
                timestamp=datetime.now(timezone.utc) - timedelta(minutes=1),
                values={"heart_rate": 74.0},
                source="test",
            )

            EventStore(database).save(original)
            restored = EventStore(database).get(original.event_id)

            self.assertIsNotNone(restored)
            assert restored is not None
            self.assertEqual(restored.as_dict(), original.as_dict())

    def test_save_updates_existing_event(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "vireon.db"
            store = EventStore(database)
            event = PharmaEvent(
                event_id="E-UPDATE-001",
                patient_id="P-002",
                site_id="S-02",
                event_type=EventType.VITAL,
                timestamp=datetime.now(timezone.utc) - timedelta(minutes=1),
                values={"heart_rate": 70.0},
                source="test",
            )

            store.save(event)
            updated = PharmaEvent(
                event_id=event.event_id,
                patient_id=event.patient_id,
                site_id=event.site_id,
                event_type=event.event_type,
                timestamp=event.timestamp,
                values={"heart_rate": 82.0},
                source=event.source,
            )
            store.save(updated)

            restored = store.get(event.event_id)
            self.assertIsNotNone(restored)
            assert restored is not None
            self.assertEqual(restored.values["heart_rate"], 82.0)


if __name__ == "__main__":
    unittest.main()
