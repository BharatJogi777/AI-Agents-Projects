# AG-182: Agent negotiation simulator

## Purpose
A framework-independent orchestration primitive with explicit validation, deterministic behavior, and testable failure paths.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design and operational notes
The implementation keeps policy and state explicit so it can be integrated into an API or worker. Add durable storage, authentication, authorization, audit logging, metrics, tracing, and resource limits before multi-process deployment. Validate all model-generated content before side effects. This is a reference component, not a distributed production service.

Tests are authored but have not been executed in the target environment.
