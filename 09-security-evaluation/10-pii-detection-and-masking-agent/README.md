# PII detection and masking agent

A deterministic Python utility for identifying and reducing exposure of common sensitive text patterns. Pattern matching is not a substitute for a dedicated DLP system; false positives and false negatives are possible.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Review custom patterns carefully and avoid logging original unredacted values.