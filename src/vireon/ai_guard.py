from __future__ import annotations
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True, slots=True)
class ModelSpec:
    model_id: str
    version: str
    context_of_use: str
    risk_tier: str
    validation_status: str

@dataclass(frozen=True, slots=True)
class ModelGuardResult:
    model_id: str
    version: str
    status: str
    risk_flags: tuple[str, ...]
    metrics: dict[str, float]

def assess_model(spec: ModelSpec, reference: list[float], current: list[float], *, missing_reference: float = 0.0, missing_current: float = 0.0) -> ModelGuardResult:
    if not reference or not current:
        raise ValueError("reference and current samples must be non-empty")
    if any(not isfinite(x) for x in reference + current):
        raise ValueError("samples must contain finite numbers")
    ref_mean = sum(reference) / len(reference)
    cur_mean = sum(current) / len(current)
    mean_shift = abs(cur_mean - ref_mean) / max(abs(ref_mean), 1.0)
    missing_shift = abs(missing_current - missing_reference)
    flags: list[str] = []
    if mean_shift >= 0.20:
        flags.append("distribution_mean_shift")
    if missing_shift >= 0.10:
        flags.append("missingness_shift")
    if spec.validation_status.lower() != "validated":
        flags.append("validation_status_not_validated")
    return ModelGuardResult(spec.model_id, spec.version, "review" if flags else "monitor", tuple(flags), {
        "reference_mean": ref_mean, "current_mean": cur_mean,
        "relative_mean_shift": mean_shift, "missingness_shift": missing_shift,
    })
