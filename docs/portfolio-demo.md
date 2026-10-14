# VIREON: portfolio demo

This demo uses synthetic data to show rule evaluation and traceability. Do not use real patient information.

## 1. Install and test

```bash
python -m pip install -e ".[test]"
python -m unittest discover -s tests -v
```

## 2. Run a repeatable scenario

```bash
vireon simulate --scenario biomarker-signal
vireon registry list
```

Point out the input event, configured rule, generated signal and evidence reference. If demonstrating repeatability, use the same event, rules and explicit timezone-aware evaluation timestamp for both runs and compare the outputs.

## 3. Show the API

```bash
uvicorn vireon.api:app --reload
```

Open `http://127.0.0.1:8000/docs`. Use only the synthetic examples and endpoints described in the project docs.

## What this demo establishes

It can show deterministic rule behaviour, input validation, local persistence and API-level behaviour covered by the tests. It does not validate a real clinical, pharmaceutical, regulatory or trial-monitoring use case.
