# Internal REST API MCP adapter

Allowlisted route adapter with bounded HTTP requests and typed JSON results.

## Design
The integration keeps deterministic validation and provider access outside the model. Inputs are bounded, the exposed MCP tools are intentionally narrow, and tests use provider-independent logic.

## Setup
Python 3.11 or newer:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

## Run
Configure provider credentials and endpoints through environment variables as described in `app/server.py`, then:
```bash
python -m app.server
```

## Security and limitations
Use least-privilege credentials, protect the MCP transport, apply provider-side quotas, and treat returned metadata as sensitive. Review the configured endpoint and network policy before deployment. The included tests are unit tests; live provider behavior requires a separately configured integration test environment.
