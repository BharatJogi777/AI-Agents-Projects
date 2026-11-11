# AG-027 — Model output parser benchmark

A small benchmark harness measures parser throughput only after correctness checks pass. It reports operation count, elapsed wall-clock time, and operations/second, allowing JSON parsing/validation strategies to be compared on the same cases.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Use representative payload sizes and repeat runs; Python microbenchmarks are noisy and do not represent model latency or end-to-end agent performance. Local tests are authored but not yet executed.
