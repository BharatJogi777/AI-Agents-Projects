# AG-029 — Intent classification agent

Wraps an injected classifier (including an LLM-backed function) with strict intent allowlisting, confidence validation, and a human-review threshold. Model output is treated as untrusted structured data.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Confidence values emitted by language models are not automatically calibrated probabilities. Evaluate on a labelled dataset and calibrate thresholds before relying on them for automated decisions. Tests are authored but not yet executed.
