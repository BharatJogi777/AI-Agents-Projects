# 06 — Context-window Truncation Strategy

**Catalogue ID:** AG-006  
**Difficulty:** Beginner → Intermediate  
**Status:** In progress — implementation and tests authored; local execution pending.  
**Runtime:** Python 3.12+  
**External services:** None required

## Goal

Fit conversation history into a model input budget without losing the current request or corrupting tool protocol state. System instructions and the pending user request are mandatory. The newest complete turns are retained first.

## Selection policy

1. Reserve output capacity and a safety margin.
2. Validate the complete conversation structure, including tool call IDs and results.
3. Count mandatory system messages and the pending current user request.
4. Fail explicitly if mandatory context exceeds the input budget.
5. Walk completed turns newest-to-oldest and keep only a contiguous suffix.
6. Treat each complete turn as atomic, including all tool calls, tool results, and the final assistant answer.
7. Recount the returned messages and assert the budget invariant.

## Architecture

```text
Conversation messages
        |
        v
Validate turns + tool call/result IDs
        |
        v
Count mandatory system + current request
        |
        +---- overflow? --> explicit error
        |
        v
Select newest complete turns atomically
        |
        v
Recount and return retained context + dropped IDs
```

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
python -m app.main
pytest
```

Optional tokenizer adapter:

```bash
pip install -e '.[tokenizer]'
```

The demo uses a character-based heuristic. It is not model-tokenizer exact. For production, inject the tokenizer matching the target model or provider.

## Example

```python
from app.token_counting import HeuristicTokenCounter
from app.truncation import ContextMessage, ContextTruncator, TruncationConfig

planner = ContextTruncator(
    HeuristicTokenCounter(),
    TruncationConfig(context_window_tokens=8192, reserved_output_tokens=1024, safety_margin_tokens=256),
)
result = planner.truncate([
    ContextMessage("system", "You are a careful assistant."),
    ContextMessage("user", "Earlier question", "turn-1"),
    ContextMessage("assistant", "Earlier answer", "turn-1"),
    ContextMessage("user", "Current question", "turn-2"),
])
```

## Important boundaries

- Tool-call messages and their matching results are kept or dropped as a whole turn. Oversized tool output causes its turn to be dropped; this module does not slice arbitrary text or JSON.
- Multimodal payloads, provider tool-schema overhead, and hidden serialization metadata require provider-aware accounting.
- The heuristic counter is for demos only. Use an official tokenizer/count API for strict context limits.
- This module does not summarize history or invoke an LLM. Summarization should be a separate explicit step with its own validation.

## Relationship to adjacent projects

- AG-004 manages persisted session history by turn count.
- AG-005 estimates tokens and prioritizes context items.
- AG-006 chooses a contiguous recent history under a hard input budget while preserving tool protocol integrity.
