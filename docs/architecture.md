# VIREON Architecture — V0.1

## Goal

V0.1 establishes a small, deterministic vertical slice of the future VIREON platform.

## Data flow

```
Synthetic source
      ↓
 PharmaEvent
      ↓
 Event validation
      ↓
 Deterministic signal rules
      ↓
 Signal
```

## Design principles

1. **Synthetic-first:** no patient data is required for development.
2. **Validation before inference:** malformed events are rejected before signal processing.
3. **Deterministic baseline:** early signal rules are explicit and testable.
4. **Human-in-the-loop:** a signal is an alert for review, never an autonomous medical decision.
5. **Traceability:** each signal references the source event that caused it.

## Planned V0.2 boundary

V0.2 will move this core behind a REST API and persistence layer. The domain objects in V0.1 are deliberately framework-light so that the core can be reused by the API, streaming layer, batch jobs, and future evidence graph.
