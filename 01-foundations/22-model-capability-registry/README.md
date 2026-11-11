# AG-022 — Model capability registry

An explicit in-memory catalogue of provider/model capabilities. Selection uses verified metadata rather than guessing from model names and returns a stable ordering.

## Architecture
- `model_registry/contracts.py`: immutable capability record and validation.
- `model_registry/registry.py`: duplicate-safe registration, lookup, filtering, and deterministic sorting.
- `app.py`: compatibility facade.

## Execution flow
Register a model with provider IDs, context/output limits, and explicit feature flags. A caller requests required features and a minimum context; the registry returns only matching models, sorted by descending context and then model ID.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Populate metadata from verified provider documentation or runtime probes. Capabilities can change across model versions. Tests are authored; local execution remains pending.
