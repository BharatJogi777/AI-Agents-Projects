"""Compatibility facade; implementation lives in idempotent_tools."""
from idempotent_tools import IdempotencyConflict,IdempotencyExecutionError,IdempotentExecutor,Record,fingerprint
__all__=["IdempotencyConflict","IdempotencyExecutionError","IdempotentExecutor","Record","fingerprint"]
