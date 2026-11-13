# AG-190: Workflow event streaming API

## Purpose
Provides an ordered, replayable in-memory event stream per workflow, with sequence cursors suitable for polling or adapting to SSE/WebSocket transports.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design
Each workflow has an independent monotonically increasing sequence. Replay uses an exclusive cursor: `after_sequence=0` returns the first event. The implementation copies the payload dictionary on publish and returns immutable event records.

## Production considerations
This implementation is process-local. For production streaming, persist events transactionally (for example, an event table or broker), authorize subscribers per workflow, bound retention, handle slow consumers, and expose heartbeats/reconnect cursors in the transport layer. Do not assume in-memory ordering spans multiple processes.

Tests are authored but have not been executed in the target environment.