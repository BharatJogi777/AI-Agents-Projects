# AG-044 — Agent cancellation handler

A cooperative cancellation token for long-running agent loops. It is thread-safe, first-reason-wins, and raises a typed exception at checkpoints.

```python
from agent_cancellation import CancellationToken
token=CancellationToken()
for step in plan:
    token.checkpoint()
    execute(step, cancellation=token)
```

A request thread may call `token.cancel("user requested stop")`; `wait(timeout)` supports blocking coordination. Cancellation cannot forcibly stop arbitrary Python or interrupt a blocking tool that ignores the token. Propagate it to tools and configure network/database timeouts. Distributed workers need shared cancellation state.

Test: `python -m pip install pytest && pytest`.
