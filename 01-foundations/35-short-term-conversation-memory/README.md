# AG-035 — Short-term conversation memory

Maintains a bounded chronological message window, retaining system instructions and evicting complete user/assistant turns rather than truncating half a turn.

## Modules
- `conversation_memory/contracts.py`: immutable message DTO.
- `conversation_memory/memory.py`: validation, thread-safe append, complete-turn eviction, snapshots, and clear.
- `app.py`: compatibility facade.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This is a message-count budget, not a tokenizer-based token budget. Add token estimation and explicit overflow policy for production model context windows. Local test execution remains pending.