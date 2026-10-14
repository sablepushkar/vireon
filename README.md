# VIREON

[![Tests](https://github.com/sablepushkar/vireon/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sablepushkar/vireon/actions/workflows/ci.yml)

VIREON is a student project I use to explore how pharmaceutical-style event data can be checked with simple rules and traced through a local workflow. The examples are synthetic. I built it to practise Python, validation, APIs, persistence and repeatable testing—not to make claims about a real pharmaceutical system.

## What is included

- Validated event objects and deterministic threshold rules.
- Local SQLite storage for the prototype.
- Evidence references and audit-style records.
- A small registry for data, models and detector configurations.
- Synthetic lifecycle scenarios.
- Command-line commands, a FastAPI API and a basic browser dashboard.
- Tests for validation, storage, API behaviour and repeatable signal evaluation.

## Workflow

```text
Synthetic event
      ↓
Input validation
      ↓
Configured deterministic rules
      ↓
Signal linked to its source event
      ↓
Local storage, evidence references and review
```

A rule-based signal can be explained by checking its input and configured threshold. Those decisions do not require a machine-learning model.

## First run

Python 3.11 or newer is recommended.

```bash
python -m pip install -e ".[test]"
python -m unittest discover -s tests -v
vireon simulate --scenario biomarker-signal
vireon registry list
```

To start the API, run `uvicorn vireon.api:app --reload`, then open `http://127.0.0.1:8000/docs` or the local `/dashboard` route. See the [portfolio demo guide](docs/portfolio-demo.md), [architecture](docs/architecture.md) and [data model](docs/data-model.md).

For repeatable signal evaluation, I can supply an explicit timezone-aware `evaluated_at` timestamp. The same event, rules and timestamp should produce repeatable results.

## Limits

VIREON uses synthetic data and local prototype infrastructure. It does not diagnose, recommend treatment, make clinical decisions, predict regulatory approval or establish regulatory compliance. A monitoring flag is a software-generated signal, not proof of misconduct. Do not use real patient data. I am keeping the project small and testing current behaviour before adding more services or machine-learning features.

---

Copyright © 2026 Pushkar Sudam Sable. See [COPYRIGHT.md](COPYRIGHT.md) for ownership and license notes.
