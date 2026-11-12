# AG-045 — Run budget and step limiter

Tracks three independent agent-run budgets: maximum steps, elapsed wall-clock duration (measured with a monotonic clock), and estimated cumulative cost.

```python
from run_budget import Budget,RunBudget
budget=RunBudget(Budget(max_steps=12,max_seconds=30,max_cost=0.05))
budget.consume(estimated_cost=0.002)  # call before each model/tool step
print(budget.snapshot())
```

A failed budget check does not consume a step or cost. Cost is an estimate supplied by the caller; this module does not calculate token/provider pricing. Check before and after expensive operations and use provider timeouts—the budget cannot preempt a synchronous call. For distributed execution, persist budget reservations atomically.

Test: `python -m pip install pytest && pytest`.
