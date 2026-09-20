from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from ..core.models import EventType, EvidenceLink, PharmaEvent


class EventStore:
    """Small SQLite event and provenance store for the V0.3 prototype."""

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
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS evidence_links (
                    evidence_id TEXT PRIMARY KEY,
                    signal_id TEXT NOT NULL,
                    event_id TEXT NOT NULL,
                    relationship TEXT NOT NULL,
                    detector_version TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(event_id) REFERENCES events(event_id)
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_evidence_signal
                ON evidence_links(signal_id)
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

    def save_evidence(self, evidence: EvidenceLink) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO evidence_links (
                    evidence_id,
                    signal_id,
                    event_id,
                    relationship,
                    detector_version,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(evidence_id) DO UPDATE SET
                    signal_id = excluded.signal_id,
                    event_id = excluded.event_id,
                    relationship = excluded.relationship,
                    detector_version = excluded.detector_version,
                    created_at = excluded.created_at
                """,
                (
                    evidence.evidence_id,
                    evidence.signal_id,
                    evidence.event_id,
                    evidence.relationship,
                    evidence.detector_version,
                    evidence.created_at.isoformat(),
                ),
            )

    def list_evidence(self, signal_id: str) -> list[EvidenceLink]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT evidence_id, signal_id, event_id, relationship,
                       detector_version, created_at
                FROM evidence_links
                WHERE signal_id = ?
                ORDER BY created_at ASC
                """,
                (signal_id,),
            ).fetchall()

        return [
            EvidenceLink(
                evidence_id=row["evidence_id"],
                signal_id=row["signal_id"],
                event_id=row["event_id"],
                relationship=row["relationship"],
                detector_version=row["detector_version"],
                created_at=datetime.fromisoformat(row["created_at"]),
            )
            for row in rows
        ]

    @staticmethod
    def _from_payload(payload: dict[str, object]) -> PharmaEvent:
        values = payload["values"]
        if not isinstance(values, dict):
            raise ValueError("stored event values must be an object")

        return PharmaEvent(
            event_id=str(payload["event_id"]),
            patient_id=(
                None
                if payload.get("patient_id") is None
                else str(payload["patient_id"])
            ),
            site_id=str(payload["site_id"]),
            event_type=EventType(str(payload["event_type"])),
            timestamp=datetime.fromisoformat(str(payload["timestamp"])),
            values=values,
            source=str(payload["source"]),
        )
