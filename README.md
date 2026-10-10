# VIREON — STUDY A.

**Pharmaceutical Lifecycle Intelligence Engine**

VIREON is a research-and-engineering prototype for connecting event data, deterministic signals, evidence provenance, audit records, and simulated pharmaceutical-development workflows. I am building it around a practical question: can a reviewer trace why a signal appeared, which input it came from, and what checks ran around that data?

## Current working ground

- Validated pharmaceutical event objects and deterministic threshold signals.
- SQLite persistence for the local prototype.
- Evidence links/graph and audit records.
- Data/model registry and reproducible evidence manifests.
- Distribution checks, digital-measure validation, and trial-site integrity indicators.
- Synthetic lifecycle scenarios and a command-line interface.
- FastAPI endpoints and a small browser dashboard.
- FHIR/OMOP mapping boundaries that are explicitly not production terminology integrations.

## The main flow

```text
Synthetic or submitted event
        ↓
Domain validation
        ↓
Versioned deterministic detector
        ↓
Signal + evidence reference
        ↓
Persistence / audit / manifest
        ↓
Human review in API or dashboard
```

The components are intentionally deterministic at this stage. A reviewer should be able to reproduce a result without needing an opaque model call.

## Quick start

Requires Python 3.11+.

```bash
python -m pip install -e ".[test]"
python -m unittest discover -s tests -v
vireon simulate --scenario biomarker-signal
vireon registry list
uvicorn vireon.api:app --reload
```

Then open `http://127.0.0.1:8000/docs` or the local `/dashboard` route. See `docs/demo.md` for a repeatable walkthrough.

## STUDY A. — focus of this update

This pass strengthens the boring-but-important boundary checks: numeric values and thresholds must be finite, and extreme numeric inputs must not crash signal detection during float conversion. Invalid values should be rejected or safely ignored according to the existing API contract, not turn into an unhandled overflow.

## Boundaries

VIREON uses synthetic data and local prototype infrastructure. It does not diagnose, recommend treatment, make autonomous clinical decisions, predict regulatory approval, or claim regulatory compliance. Trial-integrity and monitoring outputs are software review flags, not proof of trial misconduct or clinical validity. Do not use real patient data.

## Practical next steps

1. Keep input validation and API error behavior covered by regression tests.
2. Add stable, machine-readable evaluation fixtures for each signal type.
3. Improve reproducibility metadata before adding statistical or ML complexity.
4. Keep interoperability mappings explicit about unmapped fields and terminology gaps.
5. Add deployment and observability only when the local workflow is reliable.

See `DEVELOPERS_NOTES.md` for implementation details and checks.
