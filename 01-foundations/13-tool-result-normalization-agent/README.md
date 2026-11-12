# AG-013 — Tool result normalization

A serialization boundary between in-process tool results and model/API-facing JSON. It redacts common credential keys, handles cycles and dates, avoids arbitrary object representations, and enforces depth, item, string, warning, and total-byte budgets.

## Architecture

- `result_normalizer/policy.py`: immutable resource limits validated at construction.
- `result_normalizer/normalize.py`: safe recursive conversion, key-based redaction, cycle detection, warning collection, and final byte-budget enforcement.
- `result_normalizer/__init__.py`: public API.
- `app.py`: compatibility facade retaining the original keyword arguments.
- `tests/test_normalize.py`: deterministic tests; no LLM or network required.

## Execution flow

1. Accept only JSON-safe scalar types and explicitly supported date/time, Decimal, UUID, and bytes values.
2. Traverse built-in dictionaries, lists, and tuples with an active-object set to detect cycles.
3. Redact sensitive mapping keys before descending into their values.
4. Replace unsupported objects with type metadata; never call arbitrary `repr()` or custom serialization methods.
5. Bound depth, string lengths, items per container, warning count, and final UTF-8 output bytes.
6. If the complete envelope exceeds the byte budget, return a compact omission envelope instead of forwarding a partial or invalid JSON document.

## Example

```python
from result_normalizer import normalize_tool_result

tool_result = {
    "status": "ok",
    "records": [{"id": 7, "name": "payment"}],
    "access_token": "never-forward-this",
}

safe_result = normalize_tool_result(tool_result)
# safe_result["data"]["access_token"] == "[REDACTED]"
```

## Run and test

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Tests are authored; local execution remains pending.

## Security limitations

Redaction is key-based and cannot identify every secret embedded in free text, nested strings, or domain-specific fields. The key list is a baseline, not a guarantee. Do not put credentials in tool results. Add domain-specific classification before normalization when handling sensitive data. This utility does not provide authorization or prevent a trusted handler from performing unsafe actions.
