# 05 — Token Budget Estimator

**Catalogue ID:** AG-005  
**Difficulty:** Beginner → Intermediate  
**Status:** In progress — implementation and deterministic tests committed; local test execution pending.  
**Runtime:** Python 3.12+  
**External services:** None required

## Goal

Estimate how much prompt context an agent can safely send to a model. The planner accounts for the input budget left after reserving output tokens and a safety margin, then selects whole context items by priority.

This project separates counting from budget policy:

- TokenCounter is a replaceable interface.
- HeuristicTokenCounter is a dependency-free approximation for learning and local demos.
- BudgetPlanner applies deterministic admission rules; it does not know which model is running.

The heuristic is not an exact tokenizer. Tokenization varies by model, tokenizer version, language, and content. For production, inject the tokenizer that matches the target model or use the provider's authoritative token-usage/counting facility where available.

## Budget equation

~~~text
available_input_tokens =
    context_window_tokens
    - reserved_output_tokens
    - safety_margin_tokens
~~~

Each item is counted independently with a configurable per-item framing overhead. Mandatory items are admitted first. Optional items are then considered by descending priority; ties preserve input order. Items are never silently truncated: each one is either included whole or reported as dropped.

## Architecture

~~~text
Context items (system, user, history, retrieval, tools)
                    |
                    v
              TokenCounter
                    |
                    v
             BudgetPlanner
              /         \
     mandatory first   optional by priority
              \         /
                    v
         BudgetPlan (included + dropped)
~~~

## Setup

~~~bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
~~~

## Run the example

~~~bash
python -m app.main
python -m app.main --context-window 4096 --output-reserve 512 --safety-margin 128
~~~

The example prints a JSON plan showing the available input budget, estimated token use, included items, dropped items, and remaining capacity.

## Run tests

~~~bash
pytest
~~~

Tests use deterministic counters and do not need Ollama, credentials, or network access.

## Example integration

~~~python
from app.budget import BudgetConfig, BudgetPlanner, ContextItem
from app.token_counting import HeuristicTokenCounter

planner = BudgetPlanner(
    counter=HeuristicTokenCounter(chars_per_token=4),
    config=BudgetConfig(
        context_window_tokens=8192,
        reserved_output_tokens=1024,
        safety_margin_tokens=256,
    ),
)
plan = planner.plan([
    ContextItem("system", "system", "You are a careful assistant.", priority=100, mandatory=True),
    ContextItem("user", "user", "Explain the incident.", priority=100, mandatory=True),
    ContextItem("history-1", "history", "Earlier conversation...", priority=20),
    ContextItem("retrieval-1", "retrieval", "A retrieved document excerpt...", priority=10),
])
~~~

## Important boundaries

- A heuristic estimate is not a guarantee that a provider will accept the request.
- Message framing, tool schemas, image/audio payloads, and provider-specific metadata may consume additional context. Model those explicitly in a real adapter.
- Keep output reservation separate from input usage; do not allocate the full context window to the prompt.
- A mandatory-context overflow raises an error. The caller must decide whether to summarize, reject, or request a larger context window.
- The planner does not call an LLM and does not summarize or mutate content.

## Next project

AG-006 builds on this foundation by implementing context-window truncation strategies, including preserving recent turns and dropping lower-value context safely.
