# AG-013 — Tool result normalization

A serialization boundary between arbitrary in-process tool results and model/API-facing JSON. It redacts common credential keys, handles cycles and dates, avoids arbitrary object representations, and enforces depth, item, string, and total-byte budgets.

## Architecture

- `result_normalizer/policy.py`: immutable limits validated at construction.
- `result_normalizer/normalize.py`: recursive conversion, redaction, cycle detection, and final byte-budget enforcement.
- `app.py`: compatibility facade retaining the original keyword arguments.

## Execution flow

1. Convert supported scalar/date/byte values to JSON-safe values.
2. Traverse mappings and sequences with an active-object set to detect cycles.
3. Redact sensitive mapping keys before descending into their values.
4. Replace unsupported objects with type metadata; never call `repr()` on arbitrary objects.
5. Serialize the envelope and replace oversized payload data with a small omission marker.

## Run and test

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Redaction is key-based and cannot identify every secret embedded in free text. Apply domain-specific classification and avoid placing credentials in tool results. Tests are authored; local execution remains pending.
