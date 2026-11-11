# AG-022 — Model capability registry

Store explicit model/provider capability metadata and select compatible models using required features and context limits. Selection is deterministic and never infers capabilities from a model's name.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Populate the registry from verified provider documentation or runtime probes. Metadata can become stale; do not assume tool or JSON-schema support across model versions. Tests are authored but not yet executed.
