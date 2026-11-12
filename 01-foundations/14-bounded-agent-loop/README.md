# AG-014 — Bounded agent loop

A framework-independent controller that enforces independent iteration, total tool-call, per-step tool-call, consecutive-error, and total-error budgets around an agent's single-iteration callback.

## Why this exists

An agent loop is not just `while not done`. A model can repeatedly request tools, return unusable outputs, or fail over and over. Without independent budgets, one request can consume unbounded model calls, tool executions, time, and money.

This project owns loop accounting. It does not implement an LLM provider, tool registry, timeout manager, or cancellation system; those are separate components in this repository.

## Architecture

- `agent_loop/contracts.py`: immutable configuration, validated step results, typed termination exceptions, and report contracts.
- `agent_loop/runner.py`: the bounded controller and independent budget accounting.
- `agent_loop/__init__.py`: stable package exports.
- `app.py`: backward-compatible imports for the original tutorial.
- `tests/test_loop.py`: deterministic unit tests without a model or network.

## Execution flow

1. The application provides a callback that performs exactly one agent iteration.
2. The controller invokes it with a one-based step number.
3. The callback returns a `StepResult` containing actual tool-call and error counts, an optional final flag, and a value.
4. The controller validates the result and checks the per-step tool-call budget before updating totals.
5. It checks the total tool-call budget, total error budget, and consecutive error budget independently.
6. A final answer or error threshold returns a `LoopReport`; exhausting all steps without a final answer raises `AgentStepLimitExceeded`.

## Example

```python
from agent_loop import LoopConfig, StepResult, run_bounded_loop

def one_agent_iteration(step_number: int) -> StepResult:
    # Replace this deterministic example with one model/tool iteration.
    if step_number == 1:
        return StepResult(tool_calls=1, value={"status": "working"})
    return StepResult(final=True, tool_calls=1, value={"answer": "complete"})

report = run_bounded_loop(
    one_agent_iteration,
    LoopConfig(
        max_steps=5,
        max_tool_calls=8,
        max_tool_calls_per_step=3,
        max_consecutive_errors=2,
        max_total_errors=4,
    ),
)
print(report)
```

## Run and test

Requires Python 3.12+.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

No Ollama service or network is required for the unit tests. Tests are authored; local execution remains pending.

## Production integration

The callback should report actual calls, not the number the model merely proposed. A tool call rejected before dispatch should not be counted as an executed call; track rejected attempts separately if they matter to policy. If the callback dispatches tools concurrently, it must wait for or safely account for all started tasks before returning.

The controller deliberately lets provider and infrastructure exceptions propagate. A production API layer should classify those exceptions and create a terminal failure report or HTTP response without blindly retrying. Per-tool timeout, request-wide deadline, cancellation, concurrency, rate limits, and durable audit are separate controls; a step budget does not replace them.

## Limitations

The callback is trusted application code. This controller cannot interrupt a callback that hangs forever. Use the timeout/cancellation components in the later projects and an execution runtime that supports cooperative cancellation. The report is in-memory and is not a durable audit record.
