# Queue backlog diagnosis agent

Explain queue growth using backlog, arrival, processing, retry, and dead-letter metrics.

## Safety boundary

This project analyzes supplied metric/configuration snapshots only. It does not connect to production services or perform remediation.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## Limitations

Outputs are deterministic triage guidance based on caller-provided evidence. Validate findings against authoritative telemetry, platform configuration, and operational runbooks.
