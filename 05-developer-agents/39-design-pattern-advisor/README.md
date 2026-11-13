# Design pattern advisor

## Purpose
A deterministic developer-assistance utility with a narrow, reviewable API. It analyzes explicit inputs and does not automatically modify a repository.

## Run
```bash
python -m pip install -e '.[dev]'
pytest
```

## API
See `app/pattern_advisor.py` for public functions and return structures. Invalid inputs raise `ValueError`.

## Limitations and safety
Outputs are advisory. Validate findings against runtime behavior and repository conventions; review generated plans and documentation before publishing.
