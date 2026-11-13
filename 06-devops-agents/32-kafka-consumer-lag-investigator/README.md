# Kafka consumer lag investigator

Rank consumer groups by partition lag and identify stalled or imbalanced consumption.

## Safety boundary

This project analyzes supplied metric/configuration snapshots only. It does not connect to production services or perform remediation.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## Limitations

Outputs are deterministic triage guidance based on caller-provided evidence. Validate findings against authoritative telemetry, platform configuration, and operational runbooks.
