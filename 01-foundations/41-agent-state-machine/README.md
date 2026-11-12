# AG-041 — Agent state machine

A thread-safe finite-state machine for one agent run. Legal flow: created → running ↔ waiting; running → succeeded/failed/cancelled. A created run may be cancelled. Terminal states are immutable.

```python
from agent_state_machine import AgentStateMachine,State
run=AgentStateMachine()
run.transition(State.RUNNING,"worker started")
run.transition(State.WAITING,"tool call")
run.transition(State.RUNNING)
run.transition(State.SUCCEEDED)
print(run.history())
```

Each transition is a frozen, timestamped event with a monotonic sequence number. State changes and history snapshots use an RLock. Inject a clock for deterministic tests. This is process-local; persist events transactionally for distributed workers.

Test: `python -m pip install pytest && pytest`.
