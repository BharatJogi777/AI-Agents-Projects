# AG-016 — Tool timeout handler

Executes one asynchronous tool call under a per-tool timeout and an optional request-wide monotonic deadline. It distinguishes a timeout created by this wrapper from a `TimeoutError` raised by the handler itself, and propagates external cancellation.

## Architecture

- `tool_timeout/runner.py`: validates limits, applies an `asyncio.timeout` scope, combines tool and request deadlines, and measures elapsed time.
- `tool_timeout/errors.py`: distinct `ToolTimedOut` and `RequestDeadlineExceeded` exceptions.
- `app.py`: backward-compatible facade.
- `tests/test_timeout.py`: async unit tests without network services.

## Execution flow

1. Validate that the configured tool timeout is finite, positive, and no more than 300 seconds.
2. Require an async function or async callable object.
3. Read the event loop's monotonic clock.
4. If a request deadline is supplied, calculate its remaining time and choose the earlier deadline.
5. Await the handler inside an `asyncio.timeout` scope.
6. If this timeout scope expired, raise the corresponding typed timeout exception. If the handler raised its own `TimeoutError`, propagate it unchanged.
7. External `CancelledError` is not swallowed.

## Example

```python
import asyncio
from tool_timeout import execute_with_timeout, ToolTimedOut

async def fetch_customer(customer_id: str):
    await asyncio.sleep(0.2)  # Replace with an async HTTP/database client.
    return {"customer_id": customer_id}

async def main():
    loop = asyncio.get_running_loop()
    request_deadline = loop.time() + 2.0

    try:
        result = await execute_with_timeout(
            fetch_customer,
            "cust-123",
            timeout_seconds=0.5,
            deadline_at=request_deadline,
        )
        print(result.value, result.elapsed_seconds)
    except ToolTimedOut:
        print("This tool exceeded its own timeout")

asyncio.run(main())
```

## Run and test

Requires Python 3.12+.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Tests require no model, database, or network. Tests are authored; local execution remains pending.

## Important cancellation semantics

Asyncio cancellation is cooperative. The timeout cancels the task at an await point. A coroutine that catches and suppresses `CancelledError` can delay or defeat timely cancellation; handlers must not swallow cancellation. Cancellation also cannot undo a side effect already committed by a remote service. Use downstream HTTP/database deadlines, idempotency keys, and compensating actions where needed.

This module intentionally accepts async handlers only. Do not wrap blocking synchronous work directly in the event loop. `asyncio.to_thread` prevents event-loop blocking, but cancelling its await does not kill the underlying thread. For untrusted or non-cooperative blocking code, use a managed worker process or external job runtime with hard execution limits.

The request deadline must come from the same event loop's monotonic clock (`loop.time()`), not wall-clock timestamps such as `time.time()`. This module does not provide concurrency limits, retries, circuit breakers, process isolation, or distributed cancellation.
