# VIREON Portfolio Demonstration

VIREON is a repeatable synthetic-data demonstration of the complete V1.0 architecture.

## Start
Run: uvicorn vireon.api:app --reload
Open: http://127.0.0.1:8000/docs

## Flow
1. POST a synthetic lab_result with biomarker_x = 135.
2. POST /v1/signals/detect.
3. GET /v1/signals/{signal_id}/evidence.
4. GET /v1/evidence/graph.
5. POST /v1/ai-guard/assess with reference [100,100,100] and current [130,130,130].
6. POST /v1/digital-measures/validate with some missing values.
7. POST /v1/trial-integrity/sites/{site_id}/assess with a synthetic protocol deviation.
8. GET /v1/lifecycle/{candidate_id}.

## Interview points
Explain provenance, versioned analytical logic, human review, synthetic data, replaceable infrastructure adapters, and the distinction between monitoring indicators and clinical conclusions.


## V1.1 additions

Signal detection now persists signal and evidence lineage. The audit endpoint exposes event, signal, and evidence records. Interoperability endpoints project synthetic events toward FHIR Observation and an OMOP-shaped mapping boundary without claiming terminology mapping or certification.
