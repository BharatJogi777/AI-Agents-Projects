# AG-425: Answer relevance evaluator

Estimate answer coverage against a caller-provided set of required topics using normalized token overlap. Exposes missing topics and avoids claiming semantic understanding.

## Run

```bash
python -m pip install -e ".[dev]"
pytest
```

This is a deterministic lexical heuristic, not a semantic relevance model. Review consequential evaluations with domain-specific checks.