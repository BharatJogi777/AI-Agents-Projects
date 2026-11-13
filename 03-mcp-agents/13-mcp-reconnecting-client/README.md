# AG-113 — MCP reconnecting client

A small retry policy for MCP requests that fail due to transient transport errors.

## Behavior

- Retries only exception types explicitly classified as transient.
- Uses capped exponential backoff with configurable jitter.
- Preserves the final exception after attempts are exhausted.
- Does not retry invalid arguments, authorization failures, or tool-level errors unless the caller incorrectly classifies them as transient.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## MCP integration

Wrap a single request operation that uses a currently connected SDK session. If the SDK session becomes unusable, the operation/factory layer must establish a new transport and session before retrying. Do not retry non-idempotent tool calls blindly: use request idempotency keys or restrict retries to safe reads.

## Production considerations

Add retry budgets, metrics, tracing, circuit breaking, and a shared deadline. Avoid stacking this policy with SDK, proxy, and application retries because multiplicative retries can overload an unhealthy upstream.

## Limitations

This module does not create or reconnect an MCP transport itself; it provides the bounded policy around an injected operation. Tests are authored but not yet executed here.
