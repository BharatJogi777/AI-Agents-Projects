# AG-490: Meeting follow-up assistant

Convert supplied meeting notes into attributed action items, decisions, and unresolved questions; never infer an owner or deadline.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Only explicitly supplied notes and attribution are used. Missing owners and due dates are flagged for confirmation; no messages are sent. Tests are authored but have not been executed in this repository workflow.
