# VIREON

**VIREON — Pharmaceutical Lifecycle Intelligence Engine**

I built VIREON as a research and engineering project around one question: what would it look like to keep evidence, signals, data quality, model monitoring, and trial-workflow information connected across the drug-development lifecycle?

This repository is intentionally a prototype. I am using synthetic data and small deterministic components so I can inspect what each part is doing, test it, and replace pieces later with real infrastructure.

## What is in it

The current version is V1.1.

- Event ingestion and validation
- Deterministic signal detection
- SQLite persistence
- Signal and evidence provenance
- Evidence graph generation
- AI-GUARD style monitoring
- Digital-measure validation
- Trial-integrity checks
- Lifecycle simulation
- Audit records
- FHIR and OMOP interoperability boundaries

The main idea is that these are connected pieces, not separate demos.

For example:

event -> signal -> evidence -> audit

and:

data/model checks -> review flags -> human review

The project does not make a clinical decision.

## Why the first version is simple

I did not want to start by putting a large AI model in the middle of everything.

The current analytical logic is deliberately small:

- the signal engine uses explicit versioned rules;
- AI-GUARD compares reference and current distributions;
- digital measures are checked for missingness and expected ranges;
- trial integrity is represented through site-level indicators;
- lifecycle stages are treated as workflow state.

That makes it possible to test the controls first and then replace the simple logic with more advanced methods later.

## Lifecycle

Discovery -> Preclinical -> Phase I -> Phase II -> Phase III -> Regulatory -> Manufacturing -> Post-market

The lifecycle module is only a workflow simulation. It does not predict approval, recommend treatment, or claim clinical validity.

## API

Core:
- GET /health
- POST /v1/events
- GET /v1/events
- GET /v1/events/{event_id}

Signals and evidence:
- POST /v1/signals/detect
- GET /v1/signals
- GET /v1/signals/{signal_id}
- GET /v1/signals/{signal_id}/evidence
- GET /v1/evidence/graph
- GET /v1/audit

Monitoring:
- POST /v1/ai-guard/assess
- POST /v1/digital-measures/validate
- POST /v1/trial-integrity/sites/{site_id}/assess
- GET /v1/lifecycle/{candidate_id}

Interoperability boundaries:
- GET /v1/interop/fhir/events/{event_id}
- GET /v1/interop/omop/events/{event_id}

The FHIR and OMOP endpoints are mapping boundaries for the prototype. Local synthetic fields are not presented as fully mapped production terminology.

## Run it

Requires Python 3.11+.

Install:
python -m pip install -e ".[test]"

Test:
python -m unittest discover -s tests -v

Run:
uvicorn vireon.api:app --reload

Then open http://127.0.0.1:8000/docs

The repeatable walkthrough is in docs/demo.md.

## Project structure

src/vireon/
    api.py
    ai_guard.py
    digital_measures.py
    evidence_graph.py
    interop.py
    lifecycle.py
    signal_engine.py
    simulator.py
    trial_integrity.py
    core/
    storage/

tests/
docs/

## What I want to build next

The next layer is not just adding more AI. I want to make the architecture closer to a real platform that moves, checks, stores, and traces data:

- streaming/event ingestion;
- stronger statistical drift monitoring;
- device reliability analysis;
- richer trial-quality rules;
- controlled model and evidence registries;
- signed evidence manifests;
- graph-storage adapters;
- clearer FHIR/OMOP terminology mapping;
- eventually a deployable multi-service version.

## Boundaries

VIREON is a portfolio/research prototype.

It does not:
- diagnose patients;
- recommend treatment;
- make autonomous clinical decisions;
- predict regulatory approval;
- use patient data;
- claim regulatory compliance or clinical validation.

The goal is to demonstrate the engineering patterns first.

## Versions

- V0.1 — event and signal core
- V0.2 — API and persistence
- V0.3 — provenance-aware signals
- V0.4 — evidence graph
- V0.5 — AI-GUARD
- V0.6 — digital-measure validation
- V0.7 — trial-integrity engine
- V1.0 — integrated lifecycle prototype
- V1.1 — storage, audit, validation, and interoperability hardening

See CHANGELOG.md for the short history.

## License

MIT


## V2.0 portfolio layer

V2.0 adds a developer-facing layer around the V1.1 engine:

- configurable thresholds and environment settings
- reusable descriptive statistics and distribution summaries
- deterministic synthetic scenario explorer
- model/data/detector registry
- reproducible evidence manifests
- vireon command-line interface
- lightweight browser dashboard at /dashboard
- scenario API at /v1/scenarios
- registry API at /v1/registry
- manifest API at /v1/evidence/manifest/{signal_id}
- expanded portfolio documentation

### Quick demo

    pip install -e ".[test]"
    vireon simulate --scenario biomarker-signal
    uvicorn vireon.api:app --reload

Then open /dashboard.

V2.0 is intentionally a development-stage portfolio system. It demonstrates architecture, testing, provenance and domain-aware engineering rather than production clinical deployment.
