# AG-043 — Idempotent tool execution

Canonical JSON fingerprints bind idempotency keys to tool arguments. Matching retries replay the first result; conflicting reuse fails. Concurrent calls with the same key share one in-flight execution in this process.

```python
from idempotent_tools import IdempotentExecutor
executor=IdempotentExecutor()
result=executor.execute("payment-123",{"amount":25,"currency":"INR"},charge)
```

Rejects NaN/Infinity and non-JSON payloads. Failed handlers are not cached. This is not distributed exactly-once: persist the idempotency record and business effect in one transaction or use the downstream provider's idempotency key. Do not use this in-memory cache as the sole payment safety mechanism.

Test: `python -m pip install pytest && pytest`.
