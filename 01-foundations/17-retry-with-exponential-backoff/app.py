"""Backward-compatible facade; use retry_policy for new code."""
from retry_policy import RetryExhausted,RetryPolicy,retry
__all__=["RetryExhausted","RetryPolicy","retry"]
