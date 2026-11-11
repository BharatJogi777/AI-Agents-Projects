# AG-029 — Intent classification agent

Wraps an injected classifier with a fixed intent allowlist, finite confidence validation, input-size bounds, and a human-review threshold.

## Architecture
- `intent_classifier/contracts.py`: normalized intent result.
- `intent_classifier/classifier.py`: classifier invocation, schema checks, allowlist enforcement, and review decision.
- `app.py`: compatibility facade.

## Execution flow
Validate the user text, invoke the classifier, require an object containing an allowed intent and a finite confidence value in [0, 1], then mark results below the configured threshold for human review.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

LLM-reported confidence is not automatically a calibrated probability. Evaluate on a labelled dataset and calibrate the review threshold before automated use. Tests are authored; local execution remains pending.
