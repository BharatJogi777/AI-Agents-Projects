# Design notes — AG-015

## State fingerprinting

Only exact JSON-compatible Python values are accepted: null, booleans, bounded integers, finite floats, strings, lists/tuples, and dictionaries with string keys. Custom objects are not coerced through `repr`, `str`, or custom encoders. This prevents surprising application code from running during fingerprinting.

Serialization is canonicalized using sorted object keys and compact separators, then hashed with SHA-256. Input limits apply to encoded bytes, nesting depth, item count, string length, and integer bit length. Cycles and unsupported values are rejected. Tuple/list values intentionally share JSON-array semantics.

A hash is a compact equality key, not a confidentiality mechanism. Never fingerprint credentials or secrets and assume fingerprints of predictable inputs may be brute-forced.

## Rolling detector

The detector stores only recent fingerprints in a bounded deque and maintains occurrence counts for that window. With `max_repeats=2`, two prior observations are tolerated and the next (third) observation is marked repeated. When a fingerprint ages out of the window its count is decremented. The detector is protected by a lock; use one detector per agent run/session and call reset before reuse.

## Stop priority

The policy is deterministic:
1. cancellation
2. deadline exceeded
3. final answer
4. step limit
5. repeated state
6. continue

This ensures that an external cancellation is not hidden by a lower-priority heuristic and that a valid final answer is not rejected merely because the most recent state looks familiar.

## Operational boundaries

This component does not execute tools, cancel tasks, enforce wall-clock deadlines, persist state, or decide whether a repeated action is semantically safe. The agent controller supplies those signals and decides how to terminate, report, and audit the run. Snapshot design and repeat threshold require domain-specific tuning.
