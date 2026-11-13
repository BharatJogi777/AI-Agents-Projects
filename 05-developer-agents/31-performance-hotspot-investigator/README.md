# Performance hotspot investigator

## Purpose
A deterministic developer-assistance utility for focused static analysis. It returns advisory findings and does not modify source code or execute supplied code.

## Run
```bash
python -m pip install -e '.[dev]'
pytest
```

## API
Use the public `review` or `investigate` function in `app/hotspots.py`. Invalid input raises `ValueError`.

## Limitations and safety
Heuristics are intentionally conservative and cannot replace compiler diagnostics, profilers, a database query plan, or expert review. Validate each finding in its actual runtime and deployment context.
