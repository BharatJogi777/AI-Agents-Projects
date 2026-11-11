# AG-014 — Bounded agent loop

A framework-independent loop controller enforces three separate budgets: maximum reasoning/tool iterations, total tool calls, and consecutive step errors. It returns an explicit stop reason for a final answer or repeated failures. It deliberately does not decide what the model should do.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The step callback should perform one bounded model interaction and report tool/error counts. Network timeouts, per-tool authorization, and global request deadlines remain separate controls. Local test execution is pending.
