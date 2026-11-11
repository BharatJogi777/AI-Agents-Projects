# AG-027 — Model output parser benchmark

A repeatable microbenchmark harness that checks parser correctness before measuring throughput. It supports configurable iterations and warm-up runs, and returns operation count, elapsed time, and operations per second.

## Architecture
- `parser_benchmark/contracts.py`: immutable benchmark result.
- `parser_benchmark/runner.py`: correctness gate, warm-up, timed execution, and stable result ordering.
- `app.py`: compatibility facade.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Use representative payloads and repeat runs. Python microbenchmarks are noisy and do not measure model latency, network overhead, or end-to-end agent performance. Tests are authored; local execution remains pending.
