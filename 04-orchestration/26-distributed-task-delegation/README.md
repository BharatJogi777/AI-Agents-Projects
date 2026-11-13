# AG-176: Distributed task delegation

## Purpose
A deterministic delegation coordinator that assigns work to named workers, enforces worker capabilities and capacity, tracks leases, and supports bounded retries.

## Design
The implementation is a small, framework-independent orchestration component. It keeps state explicit, validates transitions at the boundary, and exposes deterministic methods that can be wrapped by an API, queue consumer, or agent runtime.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Example
See the tests for runnable examples and expected failure behavior.

## Production considerations
- Persist state and use transactional writes before running multiple processes.
- Add authentication, authorization, structured audit logs, metrics, and tracing at service boundaries.
- Define timeouts and resource limits for any external model or tool invocation.
- Treat agent output as untrusted input and validate it before side effects.

## Scope
This project provides orchestration primitives, not a distributed runtime or production message broker. Tests are authored but must be executed in the target environment before deployment.
