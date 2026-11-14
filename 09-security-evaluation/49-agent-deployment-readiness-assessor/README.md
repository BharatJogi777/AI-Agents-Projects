# Agent deployment readiness assessor

**Project ID:** AG-449

## Purpose
Assess release evidence against mandatory operational, security, privacy, and evaluation gates.

## Design
Deterministic Python utility with explicit policy inputs, structured decisions, and validation. It does not delete records, mutate audit storage, deploy agents, or execute incident-response actions.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
pytest
```

## Limitations
Treat outputs as review evidence. Production policies require legal, security, privacy, and operational ownership and should be validated against your organization's requirements.
