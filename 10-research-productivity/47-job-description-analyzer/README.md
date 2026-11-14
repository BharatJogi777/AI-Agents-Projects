# Job description analyzer

Extract explicit skills and responsibilities from a supplied job description and compare them with a caller-provided skill profile.

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
