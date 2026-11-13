# Latency and throughput benchmark

**Project ID:** AG-440

Summarize measured request durations into latency percentiles and observed throughput. The library is deterministic and consumes measurements supplied by a benchmark harness; it does not generate traffic.

## Run
```bash
pip install -e '.[test]'
pytest
```

## Limitations
Percentiles use linear interpolation over the supplied sample. Use representative load tests and report concurrency, warm-up, errors, and environment separately.