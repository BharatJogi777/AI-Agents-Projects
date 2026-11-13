# Accessible browser interaction assistant

## Purpose
A deterministic foundation for accessible browser interaction assistant workflows.

## Scope and architecture
`user-supplied observations → validation → structured result → human review`.
This repository component does not capture screens, operate a browser, record audio, or synthesize speech. Integrate those capabilities only through explicit adapters and permissions.

## Requirements and run
Python 3.10+, no runtime dependencies.
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
See `app/accessibility.py` and `tests` for examples.

## Limitations and safety
Inputs are treated as untrusted. Visual and speech interpretations can be incomplete or inaccurate. Preserve uncertainty, obtain user confirmation before actions, and provide accessible interruption and stop controls in any live integration.
