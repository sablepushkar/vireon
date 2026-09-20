from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from ..core.models import EventType, PharmaEvent


class EventStore:
    """Small SQLite event store for the V0.2 API."""

    def __init__(self, database_path: str | Path = "vireon.db") -> None:
        self._path = Path(database_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    payload TEXT NOT NULL
                )
                """
            )

    def save(self, event: PharmaEvent) -> None:
        payload = json.dumps(event.as_dict(), separators=(",", ":"))
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO events (event_id, payload)
                VALUES (?, ?)
                ON CONFLICT(event_id) DO UPDATE SET payload = excluded.payload
                """,
                (event.event_id, payload),
            )

    def get(self, event_id: str) -> PharmaEvent | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload FROM events WHERE event_id = ?",
                (event_id,),
            ).fetchone()

        if row is None:
            return None

        return self._from_payload(json.loads(row["payload"]))

    def list_events(self, limit: int = 100) -> list[PharmaEvent]:
        if not 1 <= limit <= 1000:
            raise ValueError("limit must be between 1 and 1000")

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT payload
                FROM events
                ORDER BY json_extract(payload, '$.timestamp') DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [self._from_payload(json.loads(row["payload"])) for row in rows]

    @staticmethod
    def _from_payload(payload: dict[str, object]) -> PharmaEvent:
        patient_id = payload["patient_id"]
        values = payload["values"]

        if not isinstance(values, dict):
            raise ValueError("stored event values must be an object")

        return PharmaEvent(
            event_id=str(payload["event_id"]),
            patient_id=None if patient_id is None else str(patient_id),
            site_id=str(payload["site_id"]),
            event_type=EventType(str(payload["event_type"])),
            timestamp=datetime.fromisoformat(str(payload["timestamp"])),
            values=values,
            source=str(payload["source"]),
        )
