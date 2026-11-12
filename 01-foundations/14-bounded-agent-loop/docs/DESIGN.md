# Design notes — AG-014

## Scope

The bounded loop controls agent iteration and resource counters. It is intentionally independent from any provider SDK, framework, database, or tool registry. The application owns the implementation of one iteration and reports its actual resource usage through `StepResult`.

## Independent budgets

- **Step budget:** limits the number of model/agent iterations.
- **Total tool-call budget:** limits executed tool calls across the whole run.
- **Per-step tool-call budget:** limits fan-out from a single model response.
- **Consecutive-error budget:** detects repeated failures without a successful iteration.
- **Total-error budget:** prevents intermittent errors from accumulating forever even when successes reset the consecutive counter.

A successful iteration resets only the consecutive error counter. It does not reset total errors, total tool calls, or steps.

## Accounting order

The controller validates the callback result, checks the per-step and total tool-call limits, then records counters and evaluates error/final stop conditions. It never silently clips counts to fit a budget. A callback that reports a count exceeding a limit causes a typed exception.

The controller trusts the callback's accounting. In a real agent, count calls at the actual dispatch boundary and ensure concurrent dispatches are accounted before the callback returns.

## Failure semantics

The error counters represent failures reported by the callback. Exceptions from the callback itself propagate immediately. This is deliberate: the loop must not hide provider outages, cancellation signals, programming errors, or tool-runtime exceptions by treating every exception as a model-retry opportunity.

## Report semantics

A normal report is returned when the model has a final answer or an error budget is reached. It includes aggregate counters and a bounded per-step summary. The report does not retain prompts, raw model output, tool arguments, or sensitive tool results. Exhausting the step budget without a final answer raises `AgentStepLimitExceeded`.

## Safety boundaries

This loop does not enforce wall-clock deadlines, kill blocked threads, cancel async tasks, authorize tool calls, sandbox handlers, enforce token budgets, or persist audit events. Those controls must be applied at their respective boundaries. In particular, a synchronous callback that never returns cannot be interrupted by a step counter.
