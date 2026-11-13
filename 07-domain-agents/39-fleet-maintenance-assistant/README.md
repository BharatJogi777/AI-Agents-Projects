# Fleet maintenance assistant

Flag maintenance due by odometer or elapsed time without automatically creating work orders.

## Safeguards

- Deterministic Python reference implementation; no external services or model calls.
- Recommendations do not dispatch carriers, change inventory, or authorize maintenance.
- Preserve evidence references and require operational review before execution.

## Run tests

```bash
python -m pytest
```
