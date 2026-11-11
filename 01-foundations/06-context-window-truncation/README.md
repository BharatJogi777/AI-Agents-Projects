# 06 — Context-window Truncation Strategy

**Catalogue ID:** AG-006  
**Difficulty:** Beginner → Intermediate  
**Status:** In progress — implementation and deterministic tests committed; local execution pending.  
**Runtime:** Python 3.12+  
**External services:** None required

## Goal

Fit a conversation into a model's input-token budget without corrupting its turn structure. The truncator always preserves system messages and the current user message, then retains the newest complete user/assistant turns that fit.

## Policy

1. Reserve output capacity and a safety margin.
2. Count mandatory system messages and the pending current user message.
3. Fail explicitly if mandatory context alone exceeds the input budget.
4. Walk completed turns newest-to-oldest, retaining only whole turns.
5. Stop at the first turn that does not fit. This preserves a contiguous recent history rather than cherry-picking old turns.
6. Return retained messages in their original order and report dropped turn IDs.

## Architecture

~~~text
Ordered messages
      |
      v
Validate complete user/assistant turns
      |
      v
Count system + current user (mandatory)
      |
      +--> overflow? raise explicit error
      |
      v
Walk recent complete turns backwards
      |
      v
Return ordered retained context + dropped IDs
~~~

## Setup and run

~~~bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
python -m app.main
pytest
~~~

The demo uses a deterministic character-based estimate. It is not an exact tokenizer. Inject the target model's tokenizer in production.

## Example

~~~python
from app.token_counting import HeuristicTokenCounter
from app.truncation import ContextMessage, ContextTruncator, TruncationConfig

truncator = ContextTruncator(
    HeuristicTokenCounter(),
    TruncationConfig(
        context_window_tokens=8192,
        reserved_output_tokens=1024,
        safety_margin_tokens=256,
    ),
)
result = truncator.truncate([
    ContextMessage("system", "You are a careful assistant."),
    ContextMessage("user", "Earlier question", "turn-1"),
    ContextMessage("assistant", "Earlier answer", "turn-1"),
    ContextMessage("user", "Current question", "turn-2"),
])
~~~

## Scope and limitations

- This version supports system messages and simple user/assistant turns only. Tool-call transcripts, multimodal payloads, and multi-message turns need a richer typed message model.
- It assumes input order is chronological and the final message is the pending current user request.
- It does not summarize old context or call an LLM.
- The estimator must match the target model to make reliable budget decisions; the bundled heuristic is only for demonstrations.
- If mandatory context is too large, the caller must shorten trusted instructions, use a larger context window, or apply an explicitly designed summarization step. The truncator never silently discards mandatory content.

## Relationship to adjacent projects

- AG-004 manages bounded session history by number of turns.
- AG-005 estimates context token usage and selects prioritized context items.
- AG-006 applies a recency policy to complete conversation turns under a token budget.
