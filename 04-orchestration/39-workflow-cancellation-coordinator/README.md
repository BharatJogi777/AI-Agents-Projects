# AG-189: Workflow cancellation coordinator

## Purpose
A small, framework-independent workflow orchestration primitive with explicit state, validation, and deterministic behavior.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design
The implementation is intentionally isolated from web frameworks and model providers so its behavior can be tested independently and integrated behind an API or worker.

## Production considerations
Add durable storage, distributed locking where required, authentication and authorization, structured audit logs, metrics, tracing, and operational limits before multi-process deployment. Treat external agent and tool output as untrusted input. The included implementation is an in-memory reference component, not a distributed production service.

Tests are authored but have not been executed in the target environment.
