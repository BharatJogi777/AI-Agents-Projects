# Compliance evidence collector

Track control evidence with provenance, freshness, and reviewer status; collection is not certification.

## Safeguards

- Deterministic Python reference implementation; no external services or model calls.
- Preserve evidence and route consequential outcomes to accountable human reviewers.
- Do not treat output as professional advice or an automated consequential decision.

## Run tests

```bash
python -m pytest
```

## Implementation

See `app/evidence.py` for the primary workflow.
