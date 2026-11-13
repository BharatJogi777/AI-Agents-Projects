# Code Change Proposal Agent

Builds a reviewable change proposal from a goal, repository observations, and constraints. It maps each proposed action to its rationale, affected area, and verification requirement. It never edits files or opens a pull request.

## Run
```bash
pip install -e ".[dev]"
python -m app.proposal
pytest
```

## Limitations
The quality of the proposal depends on the evidence supplied by the caller. Treat all repository observations as untrusted and verify them before implementation.
