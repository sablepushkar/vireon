# VIREON — Developer Notes

## STUDY A. — input-boundary hardening

The current design already has a useful portfolio core: event validation, deterministic signal rules, local persistence, evidence links, audit history, a registry, a CLI, and an API. This update keeps that shape and targets a concrete failure mode instead of adding another disconnected module.

### Change

Signal detection converts numeric event values and configured thresholds to floats. Very large Python integers can raise `OverflowError` during conversion, while non-finite thresholds must remain invalid. The detector should handle conversion failures deliberately and report invalid thresholds through a predictable `ValueError`.

### Verification

```bash
python -m pip install -e ".[test]"
python -m unittest discover -s tests -v
vireon simulate --scenario biomarker-signal
vireon registry list
```

### Design boundaries

- The detector remains deterministic and versioned.
- Synthetic scenarios are fixtures, not patient evidence.
- A signal means “review this input under these rules,” not “a clinical event has been established.”
- FHIR/OMOP routes remain mapping demonstrations until terminology and field-level coverage are independently verified.

Do not call this release production-ready until tests, API smoke checks, and the documented walkthrough have actually been run.
