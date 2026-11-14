# AG-493: Proposal drafting assistant

Assemble a proposal outline from user-approved project facts, scope, deliverables, milestones, and assumptions.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This deterministic reference implementation uses caller-supplied data only. Outputs require human review; it does not submit applications or contact external services. Tests are authored but have not been executed in this repository workflow.
