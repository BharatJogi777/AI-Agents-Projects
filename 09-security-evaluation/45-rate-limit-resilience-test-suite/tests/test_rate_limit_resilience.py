import pytest
from app.rate_limit_resilience import ResponseAttempt,evaluate_retries
def test_rate_limit_then_success():
 r=evaluate_retries([ResponseAttempt(429,1.5),ResponseAttempt(200)],max_attempts=3,max_retry_after_seconds=5)
 assert r.succeeded and r.attempts==2 and r.total_wait_seconds==1.5 and r.rate_limited==1
def test_retry_bounds_and_exhaustion():
 r=evaluate_retries([ResponseAttempt(429,1),ResponseAttempt(429,2)],max_attempts=2,max_retry_after_seconds=3)
 assert not r.succeeded and r.exhausted and r.total_wait_seconds==3
 with pytest.raises(ValueError): evaluate_retries([ResponseAttempt(429,6)],max_attempts=2,max_retry_after_seconds=5)
