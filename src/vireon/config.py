from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True, slots=True)
class VireonConfig:
    database_path: Path = Path("vireon.db")
    biomarker_x_threshold: float = 130.0
    heart_rate_threshold: float = 120.0
    max_query_limit: int = 1000
    environment: str = "development"

    @classmethod
    def from_env(cls) -> "VireonConfig":
        return cls(
            database_path=Path(os.getenv("VIREON_DATABASE_PATH", "vireon.db")),
            biomarker_x_threshold=float(os.getenv("VIREON_BIOMARKER_X_THRESHOLD", "130")),
            heart_rate_threshold=float(os.getenv("VIREON_HEART_RATE_THRESHOLD", "120")),
            max_query_limit=int(os.getenv("VIREON_MAX_QUERY_LIMIT", "1000")),
            environment=os.getenv("VIREON_ENVIRONMENT", "development"),
        )


def load_config() -> VireonConfig:
    return VireonConfig.from_env()
