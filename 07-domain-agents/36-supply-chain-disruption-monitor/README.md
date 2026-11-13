# Supply-chain disruption monitor

Score supplier disruption events using severity and estimated impact, retaining evidence references for human assessment.

## Safeguards

- Deterministic Python reference implementation; no external services or model calls.
- Recommendations do not dispatch carriers, change inventory, or authorize maintenance.
- Preserve evidence references and require operational review before execution.

## Run tests

```bash
python -m pytest
```
