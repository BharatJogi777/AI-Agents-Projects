# AG-114 — MCP request timeout manager

Centralizes request-level timeouts and supports an absolute end-to-end deadline.

## Design

- `TimeoutPolicy` validates defaults and caps caller-requested timeouts.
- `RequestTimeoutManager.run()` applies the resolved limit with Python 3.11 `asyncio.timeout`.
- When a monotonic deadline is supplied, the operation receives no more than the remaining budget.
- Expired deadlines fail before the operation is invoked.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## MCP usage

Wrap one SDK request call. For a multi-step agent action, pass a single monotonic deadline through discovery, tool execution, and result processing so each stage consumes the same total budget rather than receiving a fresh full timeout.

## Operational notes

Record timeout counts and latency by server/tool. Choose limits from measured upstream latency and user-facing SLOs. Cancellation of the coroutine does not guarantee that a remote server has stopped processing; use protocol cancellation where supported and make side-effecting tools idempotent.

## Limitations

The manager controls local coroutine lifetime, not remote execution semantics. Tests are authored but not yet run in this environment.
