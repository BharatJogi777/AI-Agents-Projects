# AG-015 — Stop-condition and loop detector

A deterministic termination policy for agent controllers. It fingerprints bounded JSON state snapshots, detects repeated states in a rolling history, and applies an explicit priority to cancellation, deadlines, final answers, step budgets, and repetition.

## Why it matters

A model may keep asking for the same tool with the same arguments, repeat an unchanged plan, or cycle between two states. A step budget eventually stops the run, but a loop detector can stop wasteful repetition earlier. This is a heuristic: it only works when the snapshot includes the state that changes the meaning of an action.

## Architecture

- `stop_policy/fingerprint.py`: canonical SHA-256 fingerprints with strict JSON-value validation and byte/depth/item limits.
- `stop_policy/detector.py`: thread-safe bounded rolling history, repeated-state detection, and reset.
- `stop_policy/policy.py`: centralized stop priority and strict signal validation.
- `app.py`: compatibility facade.
- `tests/test_detector.py`: deterministic tests, including rolling-window and concurrent access.

## Execution flow

1. Build a state snapshot from meaningful execution state: current plan step, tool name, normalized arguments, relevant state version, and prior result identifiers.
2. Exclude credentials, tokens, personal data, raw secrets, and irrelevant volatile fields such as timestamps or random request IDs.
3. Canonically serialize the snapshot and compute its SHA-256 fingerprint.
4. Observe it in the detector's bounded rolling history.
5. Evaluate controller signals using priority: cancellation → deadline → final answer → step limit → repeated state → continue.
6. If the detector says stop, terminate the run with a structured reason and record a safe audit event.

## Example

```python
from stop_policy import LoopDetector, evaluate_stop

detector = LoopDetector(max_repeats=2, history_size=20)
snapshot = {
    "plan_step": "lookup_customer",
    "tool": "customer_lookup",
    "arguments": {"customer_id": "cust-123"},
    "state_version": 4,
}
repetition = detector.observe(snapshot)

decision = evaluate_stop(
    final_answer=False,
    cancelled=False,
    deadline_exceeded=False,
    step_count=3,
    max_steps=12,
    detector_decision=repetition,
)
if decision.stop:
    print("Stop agent:", decision.reason)
```

With `max_repeats=2`, the third occurrence of the same state is the stopping occurrence (two occurrences after the initial observation). History is a rolling window; old fingerprints age out.

## Run and test

Requires Python 3.12+.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Tests require no model, database, or network. Tests are authored; local execution remains pending.

## Production considerations

- Snapshot quality determines detection quality. Include tool arguments and state/version information that affect semantics; omit fields that change on every iteration without changing intent.
- Avoid storing raw prompts or tool results in snapshots. Fingerprints are not encryption or anonymization; low-entropy sensitive values may be guessed offline.
- A repeated action is not necessarily a bug. Some workflows legitimately poll or retry. Use a bounded repeat threshold and include attempt counters/backoff state when those actions are expected.
- Reset the detector between independent runs. Do not share one detector across unrelated user sessions.
- Keep a separate maximum-step and wall-clock deadline. Repetition detection is not a replacement for either.
