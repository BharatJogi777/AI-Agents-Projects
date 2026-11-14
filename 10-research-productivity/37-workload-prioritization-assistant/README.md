# AG-487: Workload prioritization assistant

Rank tasks transparently using urgency, impact, effort, and blocking status while preserving the reasons for each score.

## Scope

This is a deterministic Python reference implementation. It operates only on data explicitly supplied by the caller; it does not connect to calendars, email, project trackers, or meeting services and does not perform external actions.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Design notes

- Input validation is explicit and failures raise `ValueError`.
- Results are deterministic and suitable for review before downstream use.
- Integrations, persistence, authentication, and model calls are intentionally out of scope.

## Tests

The test suite covers representative successful and invalid-input cases. Tests are authored but have not been executed in this repository workflow.
