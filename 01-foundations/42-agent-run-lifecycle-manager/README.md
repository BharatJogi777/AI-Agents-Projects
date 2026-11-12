# AG-042 — Agent run lifecycle manager

A bounded, thread-safe in-memory registry with isolated run IDs, UTC timestamps, and validated state changes.

```python
from agent_run_manager import RunManager,Status
runs=RunManager(max_runs=5000)
run=runs.create()
runs.start(run.id)
completed=runs.finish(run.id,Status.SUCCEEDED)
print(completed.finished_at)
```

Records are frozen snapshots; active runs cannot be deleted; terminal status is mandatory for completion. Capacity is explicit and records are never silently evicted. The manager is process-local, not a durable distributed queue. Production workers need transactional conditional updates, persistence, and retention.

Test: `python -m pip install pytest && pytest`.
