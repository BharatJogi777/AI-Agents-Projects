# AG-67 — Metadata-filtered retrieval agent

Apply validated allowlisted metadata filters without evaluating user-supplied expressions.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

The rewrite provider is injected. Preserve the original query for auditability; query expansions are not factual evidence. Tests are authored but not locally executed.
