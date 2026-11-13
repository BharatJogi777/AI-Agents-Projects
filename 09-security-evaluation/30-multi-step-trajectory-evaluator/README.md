# Multi-step trajectory evaluator

Evaluate agent trajectories for completion, budget, and invalid transitions using explicit state sequences and allowed transition pairs.

## Run

```bash
python -m pip install -e ".[dev]"
pytest
```

This is a deterministic trajectory checker. It does not infer hidden state or judge whether a permitted action was semantically appropriate.
