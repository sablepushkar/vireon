# VIREON Architecture

## Current release: V0.3

VIREON is a synthetic-data-first research prototype for pharmaceutical lifecycle intelligence.

### V0.3 architecture

```text
Synthetic / future connected source
            |
            v
     FastAPI ingestion
            |
     validate + normalize
            |
            v
       SQLite event store
            |
            v
     deterministic signal engine
            |
      +-----+------+
      |            |
      v            v
    Signal      Evidence Link
      |            |
      +-----+------+
            |
            v
    Evidence retrieval API
```

The important design boundary is that a signal is not treated as a standalone alert. VIREON records which event produced it and which versioned detector generated it. This creates the first provenance edge for the future evidence graph.

## Why this shape

The research phase identified real-time clinical trials, digitally derived measures, and lifecycle AI governance as active areas of regulatory and technical development. VIREON therefore uses an event-first model and keeps provenance attached to analysis outputs.

V0.3 deliberately avoids requiring Kafka, Neo4j, or cloud infrastructure for the portfolio prototype. The interfaces are kept small so durable event streaming and graph storage can be added later without rewriting the domain layer.

## Next architecture increments

1. **V0.4 — Evidence Graph:** expand evidence links into a graph of event -> transformation -> detector/model -> signal -> review action.
2. **V0.5 — AI-GUARD:** add model metadata, reference datasets, drift metrics, and validation status.
3. **V0.6 — Digital Measure Validation:** add synthetic wearable/device streams and fit-for-purpose validation metrics.
4. **Later:** provide Kafka/NATS adapters, FHIR/OMOP interoperability, and multi-site/federated processing boundaries.

## Safety boundary

VIREON is a research prototype. Its signal engine demonstrates detection and provenance mechanics only; it must not be used for autonomous clinical decisions or patient care.
