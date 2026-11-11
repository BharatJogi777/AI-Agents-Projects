# AG-016 — Tool timeout handler

An async execution wrapper applies a per-tool deadline using `asyncio.wait_for`, returns a typed success envelope, and raises a dedicated timeout exception. Cancellation is propagated to the handler, so long-running async tools should use cancellation-safe cleanup.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This wrapper intentionally accepts async handlers only. Cancelling a coroutine does not guarantee that an external side effect has been rolled back; use idempotency keys and downstream deadlines. Blocking synchronous functions require process isolation or a separately managed worker—thread cancellation cannot safely terminate them. Local test execution is pending.
