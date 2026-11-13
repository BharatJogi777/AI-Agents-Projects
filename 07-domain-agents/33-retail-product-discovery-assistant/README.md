# Retail product discovery assistant

Retrieve relevant catalogue products using transparent query-term matching and deterministic ranking.

## Safeguards

- Deterministic Python reference implementation; no external services or model calls.
- Outputs are recommendations only; no bookings, purchases, inventory writes, or payment authorization.
- Validate source data and route exceptions to human review.

## Run tests

```bash
python -m pytest
```
