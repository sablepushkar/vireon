from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from vireon.api import create_app


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        database_path = Path(self.tempdir.name) / "test.db"
        self.client = TestClient(create_app(database_path))

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _payload(self, **overrides: object) -> dict[str, object]:
        timestamp = datetime.now(timezone.utc) - timedelta(minutes=1)
        payload: dict[str, object] = {
            "event_id": "E-API-001",
            "patient_id": "P-001",
            "site_id": "S-01",
            "event_type": "lab_result",
            "timestamp": timestamp.isoformat(),
            "values": {"biomarker_x": 135.0},
            "source": "test",
        }
        payload.update(overrides)
        return payload

    def test_health(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_create_and_read_event(self) -> None:
        created = self.client.post("/v1/events", json=self._payload())
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.json()["event_id"], "E-API-001")

        fetched = self.client.get("/v1/events/E-API-001")
        self.assertEqual(fetched.status_code, 200)
        self.assertEqual(fetched.json()["values"]["biomarker_x"], 135.0)

    def test_invalid_future_event_is_rejected(self) -> None:
        future = datetime.now(timezone.utc) + timedelta(hours=1)
        response = self.client.post(
            "/v1/events",
            json=self._payload(timestamp=future.isoformat()),
        )
        self.assertEqual(response.status_code, 422)

    def test_signal_detection(self) -> None:
        created = self.client.post("/v1/events", json=self._payload())
        self.assertEqual(created.status_code, 201)

        response = self.client.post("/v1/signals/detect")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["signal_count"], 1)
        self.assertEqual(body["signals"][0]["signal_type"], "biomarker_elevation")


if __name__ == "__main__":
    unittest.main()
