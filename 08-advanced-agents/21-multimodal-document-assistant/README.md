# Multimodal Document Assistant

Validate and assemble text, image, audio, and tabular document parts into a provenance-preserving review package.

## Safety boundary
This deterministic reference implementation validates supplied data and prepares a reviewable result. It does not autonomously contact external services or execute consequential actions.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
