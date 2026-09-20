# VIREON

**VIREON — Pharmaceutical Lifecycle Intelligence Engine**

VIREON is an open-source research and engineering prototype for monitoring pharmaceutical-development workflows through structured events, evidence lineage, anomaly signals, and human review.

> **Safety boundary:** VIREON is a research prototype. It uses synthetic data and does not diagnose patients, recommend treatment, or make autonomous clinical decisions.

## Current milestone

**V0.2 — API + persistent event store**

- Validated pharmaceutical/trial event model
- Deterministic synthetic event generation
- Rule-based anomaly signal detection
- FastAPI REST interface
- SQLite-backed event persistence
- Automated unit/API tests
- GitHub Actions CI

## Architecture direction

```
Synthetic / future real data
        ↓
  Event validation
        ↓
 Persistent event store
        ↓
 Signal detection
        ↓
 Evidence lineage
        ↓
 Human review
        ↓
    Audit trail
```

Future modules will add trial-integrity monitoring, AI-model monitoring, digital-measure validation, evidence graphs, and development simulation.

## Local development

Requires Python 3.11+.

```bash
python -m pip install -e ".[test]"
python -m unittest discover -s tests -v
uvicorn vireon.api:app --reload
```

API documentation is then available at `/docs`.

## Roadmap

- V0.1: event + signal core
- **V0.2: REST API + persistent database**
- V0.3: real-time event streaming
- V0.4: evidence lineage graph
- V0.5: AI-GUARD monitoring
- V0.6: digital-measure validation
- V0.7: trial-integrity engine
- V1.0: integrated pharmaceutical lifecycle intelligence platform

## License

MIT
