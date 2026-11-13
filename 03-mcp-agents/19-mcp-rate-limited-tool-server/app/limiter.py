"""Thread-safe token bucket keyed by authenticated identity and tool."""
from dataclasses import dataclass
from threading import Lock
from time import monotonic
from typing import Callable

@dataclass
class _Bucket:
    tokens: float
    updated_at: float

class TokenBucketLimiter:
    def __init__(self, *, capacity: int, refill_per_second: float, clock: Callable[[], float] = monotonic):
        if capacity < 1 or refill_per_second <= 0:
            raise ValueError("capacity and refill rate must be positive")
        self.capacity, self.refill_rate = float(capacity), refill_per_second
        self._clock, self._buckets, self._lock = clock, {}, Lock()

    def allow(self, key: str, *, cost: float = 1.0) -> bool:
        if not key.strip() or cost <= 0 or cost > self.capacity:
            raise ValueError("invalid key or token cost")
        now = self._clock()
        with self._lock:
            bucket = self._buckets.get(key, _Bucket(self.capacity, now))
            bucket.tokens = min(self.capacity, bucket.tokens + max(0.0, now-bucket.updated_at)*self.refill_rate)
            bucket.updated_at = now
            if bucket.tokens < cost:
                self._buckets[key] = bucket
                return False
            bucket.tokens -= cost
            self._buckets[key] = bucket
            return True
