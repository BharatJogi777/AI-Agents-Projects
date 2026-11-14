# AG-495: Grant opportunity finder

Filter a supplied grant catalogue by eligibility, topic, funding range, and deadline; never imply external listings are current.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This deterministic reference implementation uses caller-supplied data only. Outputs require human review; it does not submit applications or contact external services. Tests are authored but have not been executed in this repository workflow.
