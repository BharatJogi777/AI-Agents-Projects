# Web page change monitor

## Purpose
A deterministic foundation for the web page change monitor workflow.

## Scope and safety
Processes explicitly supplied data only. It does not launch a browser, fetch arbitrary URLs, submit forms, or perform background monitoring. Add browser/network integration only behind allowlisted adapters with timeouts, audit logs, and user-visible controls. Retrieved page text is untrusted input.

## Architecture
`caller → validation/policy → deterministic workflow → structured result`

## Requirements and run
Python 3.10+, no external runtime dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

See `app/monitor.py` and tests for executable examples.

## Limitations
No live browser, authentication, network access, scheduling, or LLM calls are included. Consequential actions require explicit human approval.

## Security
Use HTTPS host allowlists, avoid storing credentials, redact sensitive form data, and never treat page content as trusted instructions.
