# Resume screening workflow assistant

Compare job-related skills against candidate evidence without protected attributes or automated hiring decisions.

## Safeguards

- Deterministic Python reference implementation; no external services or model calls.
- Preserve evidence and route consequential outcomes to accountable human reviewers.
- Do not treat output as professional advice or an automated consequential decision.

## Run tests

```bash
python -m pytest
```

## Implementation

See `app/screening.py` for the primary workflow.
