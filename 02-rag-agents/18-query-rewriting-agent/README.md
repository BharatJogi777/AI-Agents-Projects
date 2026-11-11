# AG-68 — Query rewriting agent

Expand ambiguous queries using an injected rewriter while retaining the original and bounding variants.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

The rewrite provider is injected. Preserve the original query for auditability; query expansions are not factual evidence. Tests are authored but not locally executed.
