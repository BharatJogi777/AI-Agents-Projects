# Delivery route planning assistant

Validate delivery stops, coordinates, demand and vehicle capacity before downstream route optimization.

## Safeguards

- Deterministic Python reference implementation; no external services or model calls.
- Recommendations do not dispatch carriers, change inventory, or authorize maintenance.
- Preserve evidence references and require operational review before execution.

## Run tests

```bash
python -m pytest
```
