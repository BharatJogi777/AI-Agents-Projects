# Mixture-of-experts agent router

Select and combine specialist experts using validated non-negative routing weights and deterministic aggregation.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Structure
- `app/experts.py`: top-k routing and normalized weights.
- `tests/test_experts.py`: normal routing and invalid score cases.

This is a local reference implementation. Expert weights are routing preferences, not calibrated confidence or proof of correctness. Validate outputs independently before downstream side effects.
