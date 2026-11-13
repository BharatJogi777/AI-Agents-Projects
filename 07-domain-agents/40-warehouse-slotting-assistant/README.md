# Warehouse slotting assistant

Recommend warehouse zones using pick frequency and available slot capacity; do not move inventory.

## Safeguards

- Deterministic Python reference implementation; no external services.
- Recommendations are advisory and do not mutate warehouse inventory.

## Run tests

```bash
python -m pytest
```
