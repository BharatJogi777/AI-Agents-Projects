# AG-038 — Memory summarization agent

Calls an injected summarizer behind strict source and output size bounds. Exposes optional metadata about source and summary lengths without claiming that generated statements are verified facts.

## Modules
- `memory_summarizer/contracts.py`: summary metadata DTO.
- `memory_summarizer/agent.py`: summarizer protocol, input/output validation, and metadata.
- `app.py`: compatibility facade.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The summarizer may omit or distort details. Preserve source references, evaluate factual consistency, and require confirmation before promoting a generated summary into durable preference memory. Local test execution remains pending.