# AG-030 — Entity extraction agent

An injected extraction function proposes candidate entities; deterministic application code validates entity kinds, exact evidence spans, offsets, duplicates, input size, and maximum result count.

## Architecture
- `entity_extractor/contracts.py`: immutable entity record and extraction error.
- `entity_extractor/extractor.py`: model-output validation and exact source-grounding checks.
- `app.py`: compatibility facade.

## Execution flow
Pass source text to the extractor. Each returned entity must use an allowlisted kind and non-empty value/evidence. The evidence must occur exactly in the source, and the entity value must occur inside that evidence. Valid results include source offsets; duplicate candidates at the same span are removed.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Exact substring checks establish provenance, not semantic correctness or completeness. Production use should add versioned schemas, entity normalization, document IDs, and labelled evaluation. Tests are authored; local execution remains pending.
