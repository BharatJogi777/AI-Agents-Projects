# Prometheus MCP integration

A read-only MCP tool for Prometheus instant queries using PromQL.

## Features
- Validates and bounds PromQL input.
- Uses an HTTP request timeout and returns at most 500 time series.
- Exposes no mutation endpoints.
- Keeps query normalization separate for unit testing.

## Requirements
Python 3.11+. Install with `pip install -e ".[dev]"`.

## Run
Set `PROMETHEUS_URL` (default: `http://localhost:9090`) and run:
```bash
python -m app.server
```

## Security
Keep Prometheus behind a trusted network boundary and enforce authentication at the proxy. Use TLS for remote endpoints. PromQL can be computationally expensive; apply server-side query limits and rate limits. This integration is read-only but query access can still reveal sensitive operational data.

## Tests
```bash
pytest -q
```
