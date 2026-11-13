# AG-115 — MCP cancellation propagation

Provides an explicit cancellation signal for multi-stage async operations and propagates cancellation of the outer task to its child operation.

## Design

- Pass one `asyncio.Event` through planning, MCP request, and post-processing layers.
- Each layer should check/await the same signal and stop promptly.
- `run_with_cancellation` owns the operation task and cancels it if its caller is cancelled.
- `cancellable_sleep` demonstrates how a long wait can respond to the shared event.

## Run

```bash
pip install -e '.[dev]'
pytest
```

## MCP integration

The MCP SDK and transport may expose their own cancellation semantics. Adapt the shared event to the SDK's cancellation mechanism rather than assuming local task cancellation stops remote execution. For side-effecting tools, combine cancellation with idempotency and explicit operation status.

## Limitations

This helper does not send a protocol-level cancellation message or guarantee that a remote server stopped. Tests are authored; execute them locally before deployment.
