# AG-019 — Provider-agnostic LLM adapter

Defines normalized chat request/response contracts and a provider protocol. Application and agent code depend on these contracts, while concrete adapters translate provider-specific payloads. A small facade routes calls to a named/default provider and validates the response contract.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The interface intentionally models text chat only; tool calls, streaming, multimodal content, and provider-specific structured output should be added as explicit capability interfaces rather than hidden inside generic dictionaries. Local test execution is pending.
