# Shipment exception investigator

Detect late, overdue and exceptional shipments from timestamped carrier events with traceable references.

## Safeguards

- Deterministic Python reference implementation; no external services or model calls.
- Recommendations do not dispatch carriers, change inventory, or authorize maintenance.
- Preserve evidence references and require operational review before execution.

## Run tests

```bash
python -m pytest
```
