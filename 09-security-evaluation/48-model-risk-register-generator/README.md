# Model risk register generator

**Project ID:** AG-448

## Purpose
Convert structured model risk findings into a prioritized, traceable risk register with ownership and mitigation fields.

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
