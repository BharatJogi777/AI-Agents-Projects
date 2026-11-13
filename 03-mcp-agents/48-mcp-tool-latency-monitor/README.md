# MCP tool latency monitor

Measure tool-call duration without coupling telemetry to the tool implementation.

## Run
`python -m pip install -e ".[dev]"`
`pytest`

The monitor records bounded samples per tool, computes count/min/max/mean and nearest-rank p95, and supports a configurable slow-call threshold. It is an in-process demonstration; use a metrics backend for durable, multi-process telemetry.

## Design
- `app/monitor.py`: deterministic timing and aggregation.
- `app/server.py`: optional FastMCP example tool.
- Tests cover empty metrics, aggregation, thresholds, and invalid inputs.

Do not record tool arguments or returned payloads in latency telemetry; they may contain secrets or personal data.
