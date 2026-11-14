# Job search research assistant

Organize a supplied list of target employers and role leads, deduplicate entries, and preserve source provenance and follow-up status.

## Scope

A deterministic Python reference implementation that uses only information explicitly provided by the learner or caller. It does not scrape job boards, contact employers, submit applications, or claim external facts are verified.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Tests

The test suite covers normal behavior and invalid inputs. Tests are authored but have not been executed in this repository workflow.
