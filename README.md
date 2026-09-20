# VIREON

**VIREON — Pharmaceutical Lifecycle Intelligence Engine**

VIREON is a synthetic-data-first research and engineering prototype for evidence-aware pharmaceutical development workflows. It combines event ingestion, signal detection, provenance, model monitoring, digital-measure validation, trial-integrity monitoring, and lifecycle simulation.

> Safety boundary: VIREON is a portfolio/research prototype. It does not diagnose patients, recommend treatment, make regulatory decisions, or autonomously control clinical workflows. All outputs are monitoring or workflow-simulation artifacts for synthetic data.

## Complete project

V0.1 — Event + signal core: typed events, deterministic synthetic generation, validation, rule-based signals, tests.

V0.2 — API + persistence: FastAPI, SQLite persistence, event CRUD, API tests, CI.

V0.3 — Provenance-aware signals: versioned detectors, persistent evidence links, evidence retrieval, source-event traceability.

V0.4 — Evidence Graph: serializable event -> signal -> evidence graph, ready for a future graph-storage adapter.

V0.5 — AI-GUARD: context-of-use metadata, reference/current distribution monitoring, missingness-shift monitoring, explainable risk flags.

V0.6 — Digital Measure Validation: synthetic digital observations, completeness analysis, expected-range checks, review classification.

V0.7 — Trial Integrity Engine: site-level monitoring of missingness, protocol-deviation patterns, and timestamp-collision patterns.

V1.0 — Integrated Lifecycle Prototype: discovery -> preclinical -> Phase I -> Phase II -> Phase III -> regulatory -> manufacturing -> post-market representation, shared provenance, and human-review boundaries.

## API
GET /health
POST /v1/events
GET /v1/events
GET /v1/events/{event_id}
POST /v1/signals/detect
GET /v1/signals/{signal_id}/evidence
GET /v1/evidence/graph
POST /v1/ai-guard/assess
POST /v1/digital-measures/validate
POST /v1/trial-integrity/sites/{site_id}/assess
GET /v1/lifecycle/{candidate_id}

Run: uvicorn vireon.api:app --reload
Then open /docs.

## Research alignment
The architecture is aligned with current themes in pharmaceutical AI: clear context of use, risk-based assessment, data governance/documentation, lifecycle management, human-centric oversight, digital measures, and real-time trial infrastructure. FDA and EMA published joint AI practice principles in January 2026, and FDA continues active work on digital health technologies and real-time clinical trials.

VIREON does not claim regulatory compliance or clinical validity. It demonstrates engineering controls inspired by these themes.

## Development
Requires Python 3.11+.
Install: python -m pip install -e ".[test]"
Test: python -m unittest discover -s tests -v

## Portfolio demo
Use docs/demo.md for a repeatable synthetic walkthrough.

## Engineering principles
Synthetic data first; deterministic tests; explicit provenance; versioned analytical logic; explainable monitoring; human-in-the-loop boundaries; minimal dependencies; replaceable infrastructure adapters; no patient data.

## Post-V1.0 expansion
Streaming adapters, FHIR/OMOP interoperability, stronger statistical drift metrics, device reliability analysis, richer trial-quality rules, signed evidence manifests, graph-database adapters, and controlled model-registry workflows.

## License
MIT
