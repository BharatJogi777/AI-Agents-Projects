# Legal intake triage assistant

Normalize legal matter intake, flag urgency and missing information, and route for qualified human review.

## Safeguards

- Deterministic Python reference implementation; no external services or model calls.
- Preserve evidence and route consequential outcomes to accountable human reviewers.
- Do not treat output as professional advice or an automated consequential decision.

## Run tests

```bash
python -m pytest
```

## Implementation

See `app/intake.py` for the primary workflow.
