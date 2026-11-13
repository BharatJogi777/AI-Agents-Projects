# Debate and consensus workflow

Collect independent agent positions and compute a transparent consensus using a configurable quorum.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Design
- `app/consensus.py`: validates positions and computes votes.
- `tests/test_consensus.py`: majority, ties, and invalid quorum.

This reference uses equal-weight votes. It does not establish truth: consensus can be wrong, correlated agents can share the same bias, and rationales require separate evidence review. Keep final high-impact decisions under deterministic policy and human oversight.
