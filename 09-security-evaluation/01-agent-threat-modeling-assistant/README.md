# Agent threat modeling assistant

A deterministic, dependency-light security evaluation component for agent systems.

## Scope

This project provides a small, testable primitive. It does not connect to an LLM, execute tools, or prove a system secure. Use its findings as inputs to human-reviewed threat analysis and defense-in-depth testing.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Safety notes

- Treat model outputs and external content as untrusted.
- Enforce authorization at the tool server, not only in prompts.
- Keep secrets out of prompts, logs, and test fixtures.
- Extend the deterministic cases with organization-specific abuse scenarios.
