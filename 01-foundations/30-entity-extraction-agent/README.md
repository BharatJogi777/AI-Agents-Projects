# AG-030 — Entity extraction agent

An injected LLM/extractor returns candidate entities, while deterministic application code validates types, exact evidence substrings, offsets, input limits, and duplicates. The model cannot establish facts that are absent from the source text.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Exact substring evidence is a grounding check, not proof of semantic correctness or extraction completeness. For production, add a versioned schema, entity-specific normalization, document provenance, and evaluation against annotated examples. Tests are authored but not yet executed.
