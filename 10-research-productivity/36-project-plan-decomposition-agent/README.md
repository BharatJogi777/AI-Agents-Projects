# AG-486: Project plan decomposition agent

Break a project goal into ordered, dependency-aware tasks with explicit owners, estimates, and acceptance criteria.

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
