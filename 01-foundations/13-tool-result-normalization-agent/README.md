# AG-013 — Tool result normalization

Tool handlers can return datetimes, bytes, custom objects, deeply nested values, circular references, or accidental secrets. This boundary converts outputs into bounded JSON-safe envelopes, redacts common credential keys, and reports truncation/unsupported-type warnings.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The normalizer is a safety boundary, not a substitute for data classification. Add domain-specific secret fields to the redaction policy and avoid putting credentials in tool outputs in the first place. Local test execution is pending.
