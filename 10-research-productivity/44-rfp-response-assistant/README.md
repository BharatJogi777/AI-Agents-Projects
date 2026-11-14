# AG-494: RFP response assistant

Map supplied RFP questions to approved evidence, identify unanswered requirements, and flag responses needing subject-matter review.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This deterministic reference implementation uses caller-supplied data only. Outputs require human review; it does not submit applications or contact external services. Tests are authored but have not been executed in this repository workflow.
