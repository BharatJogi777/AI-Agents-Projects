# 05 — Token Budget Estimator

**Catalogue ID:** AG-005  
**Difficulty:** Beginner → Intermediate  
**Status:** Implemented planner, heuristic and optional model-tokenizer adapter; tests authored, execution pending.  
**Runtime:** Python 3.12+  
**External services:** None required

## Problem this solves

An agent cannot blindly append unlimited history, retrieved chunks and tool output to a prompt. It must budget the model's context window while reserving room for generated output and a safety margin.

The planner computes:

    available_input_tokens =
        context_window_tokens
        - reserved_output_tokens
        - safety_margin_tokens

It admits mandatory context first, then optional items by descending priority. Equal priorities preserve caller order. The returned included/dropped collections preserve original input order. Items are never silently cut.

## Architecture

    ContextItem list
         |
         v
    TokenCounter interface
       |             |
       v             v
    Heuristic     Tiktoken (optional)
       \             /
        v           v
        BudgetPlanner
             |
             v
    BudgetPlan: included + dropped + remaining capacity

### Components

- `ContextItem`: one atomic prompt component, such as system instructions, current user request, conversation turn, retrieval chunk, or tool result.
- `TokenCounter`: replaceable counting contract.
- `HeuristicTokenCounter`: dependency-free character approximation for demos. Not exact.
- `TiktokenCounter`: optional tokenizer adapter for supported OpenAI model encodings.
- `BudgetPlanner`: deterministic admission policy; it does not know about providers or call an LLM.
- `MandatoryContextOverflow`: explicit failure if mandatory items cannot fit.

## Setup

    python3.12 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -e '.[dev]'

For the optional tiktoken adapter:

    pip install -e '.[dev,tiktoken]'

## Run

    python -m app.main
    python -m app.main --context-window 4096 --output-reserve 512 --safety-margin 128

The demo emits a JSON budget plan. It uses the heuristic counter by default.

## Use the planner

    from app.budget import BudgetConfig, BudgetPlanner, ContextItem
    from app.token_counting import HeuristicTokenCounter

    planner = BudgetPlanner(
        counter=HeuristicTokenCounter(chars_per_token=4),
        config=BudgetConfig(
            context_window_tokens=8192,
            reserved_output_tokens=1024,
            safety_margin_tokens=256,
            per_item_overhead_tokens=4,
        ),
    )
    plan = planner.plan([
        ContextItem("system", "system", "You are a careful assistant.", priority=100, mandatory=True),
        ContextItem("current-user", "user", "Explain the incident.", priority=100, mandatory=True),
        ContextItem("history-1", "history", "Earlier conversation...", priority=20),
        ContextItem("retrieval-1", "retrieval", "Retrieved evidence...", priority=10),
    ])

    for entry in plan.included:
        print(entry.item.item_id, entry.estimated_tokens)
    print("Remaining:", plan.remaining_input_tokens)
    print("Dropped:", [entry.item.item_id for entry in plan.dropped])

## Use the model-specific tokenizer

    from app.token_counting import TiktokenCounter

    counter = TiktokenCounter(model="gpt-4o")
    token_count = counter.count("Count this text using the model encoding.")

Or choose an explicit known encoding:

    counter = TiktokenCounter(encoding_name="cl100k_base")

A model tokenizer counts text tokens, but provider message framing, tool schemas, multimodal payloads and hidden metadata may add tokens. Include a measured framing allowance or use authoritative provider usage/counting APIs when available.

## Selection behavior

1. Validate unique item IDs and count every item.
2. Reserve output and safety margin before planning.
3. Admit mandatory items in caller order. If any do not fit, raise `MandatoryContextOverflow`.
4. Sort optional items by descending priority, stably for ties; admit each whole item if it fits.
5. Return selected and dropped items in original caller order.

The planner does not truncate content. A large optional item may be dropped while a smaller, lower-priority item still fits. This is intentional best-fit admission under a priority ordering, not a knapsack optimizer.

## Tests

    pytest

Tests cover budget arithmetic, mandatory overflow, stable priority selection, whole-item dropping, duplicate IDs, invalid configuration, invalid tokenizer return values, and tokenizer adapter behavior. Tests are committed but have not been executed in this environment.

## Production boundaries

- Do not use the heuristic as an exact model tokenizer.
- Token counts may differ across model versions and provider request formats.
- Configure per-item framing overhead based on the actual serialized request.
- Keep system instructions and the current user request mandatory only when the product policy requires them; mandatory overflow must be handled explicitly.
- This project plans context. It does not summarize, redact, persist, or call a model.
