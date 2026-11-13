# Retail inventory exception agent

Identify low-stock and overstock exceptions from on-hand, reserved, and target quantities.

## Safeguards

- Deterministic Python reference implementation; no external services or model calls.
- Outputs are recommendations only; no bookings, purchases, inventory writes, or payment authorization.
- Validate source data and route exceptions to human review.

## Run tests

```bash
python -m pytest
```
