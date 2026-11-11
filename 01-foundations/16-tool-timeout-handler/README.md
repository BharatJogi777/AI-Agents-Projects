# AG-016 — Tool timeout handler

Applies a deadline to one asynchronous tool invocation and distinguishes a deadline cancellation from a timeout raised by the handler itself.

## Architecture
- `tool_timeout/runner.py`: async task creation, monotonic timing, cancellation through `asyncio.wait_for`, and elapsed-time result.
- `tool_timeout/errors.py`: dedicated `ToolTimedOut` exception.
- `app.py`: compatibility facade.

## Execution flow
1. Validate the timeout and require an async handler.
2. Create a task and record a monotonic start time.
3. Await the task under the configured deadline.
4. Return a typed result on success; translate only the wrapper-triggered timeout into `ToolTimedOut`.
5. Allow handler exceptions and external cancellation to propagate.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Coroutine cancellation is cooperative; it cannot roll back an already-committed side effect. Use downstream deadlines and idempotency keys. Blocking synchronous work needs process isolation or a managed worker. Local test execution remains pending.
