# AG-010 — Multi-tool selection agent

The model selects among three application-owned tools: add two numbers, count characters, and return UTC time. Python validates typed arguments and executes the allowlisted handler. The model only plans and explains; it does not perform deterministic work.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
ollama pull qwen3:4b
python -m main "Add 12 and 30"
python -m main "How many characters are in 'agentic systems'?"
pytest
```

Tests use a fake model client and need no Ollama service. Local test execution and live model integration are pending. This CLI is a learning project, not a hosted multi-tenant service.
