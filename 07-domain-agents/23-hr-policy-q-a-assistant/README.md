# HR policy Q&A assistant

Retrieve policy passages with transparent keyword matching and citations; abstain when evidence is insufficient.

## Safeguards

- Deterministic Python reference implementation; no external services or model calls.
- Preserve evidence and route consequential outcomes to accountable human reviewers.
- Do not treat output as professional advice or an automated consequential decision.

## Run tests

```bash
python -m pytest
```

## Implementation

See `app/policy.py` for the primary workflow.
