# Design notes — AG-016

## Clock and deadline model

Timeouts are measured using the event loop's monotonic clock. Wall clocks can jump due to synchronization or administrative changes and must not be used for elapsed-time enforcement. The optional `deadline_at` is an absolute monotonic timestamp created from the same loop's `loop.time()`.

The effective timeout is the minimum of the per-tool timeout and remaining request budget. If the request deadline is already elapsed, the handler is never invoked. When both deadlines are equal, the request deadline is treated as the controlling boundary.

## Correct timeout classification

The implementation uses the expiration state of its own `asyncio.timeout` context. This matters because a handler may independently raise Python's `TimeoutError` (for example, an upstream HTTP client timeout). That error is not mislabeled as the wrapper's timeout.

## Cancellation

The timeout context cancels the current task. Cancellation propagates through the awaited coroutine chain at cooperative suspension points. Handler code should use `try/finally` for cleanup and must re-raise `asyncio.CancelledError` after cleanup. Swallowing cancellation can delay completion and break shutdown guarantees.

A timeout is not rollback. If a handler has already sent a payment or committed a database transaction, cancelling the coroutine cannot reverse that side effect. Use idempotency keys, transactional boundaries, and compensating workflows.

## Synchronous work

The public API deliberately requires an async callable. A blocking synchronous function run on the event loop blocks all other tasks and prevents the timeout from firing. Moving it to `asyncio.to_thread` keeps the event loop responsive but cannot forcibly stop the worker thread. Use a process or isolated worker service for code requiring hard termination.

## Non-goals

This component does not retry, rate-limit, queue, sandbox, or authorize tool calls. It does not enforce a global agent budget by itself; callers pass the request-wide deadline. It does not guarantee termination of a coroutine that suppresses cancellation.
