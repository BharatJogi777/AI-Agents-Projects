# Rate limit resilience test suite

**Project ID:** AG-445

Evaluate recorded HTTP response attempts for a client retry policy. The evaluator enforces an attempt budget, bounds retry-after delays, and reports success, exhaustion, and cumulative wait time without issuing network requests.

## Run
```bash
pip install -e '.[test]'
pytest
```

## Limitations
The evaluator only models HTTP 429 retries and 2xx success. Real clients must also consider jitter, idempotency, server-specific headers, and retry budgets.