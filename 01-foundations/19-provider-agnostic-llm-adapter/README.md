# AG-019 — Provider-agnostic LLM adapter

Defines a normalized text-chat contract and a provider selector. Application/agent code depends on the contract, while provider-specific request mapping stays behind an adapter implementation.

## Architecture
- `llm_adapter/contracts.py`: validated chat messages, requests, responses, and read-only metadata/usage mappings.
- `llm_adapter/provider.py`: provider protocol, explicit provider selection, and response-contract enforcement.
- `app.py`: compatibility facade.

## Execution flow
1. Construct a validated `ChatRequest`.
2. Select the configured default provider or an explicitly named provider.
3. Invoke its `chat()` implementation.
4. Reject any adapter that does not return the normalized `ChatResponse` contract.
5. Keep provider-specific capabilities (streaming, tools, vision, JSON mode) explicit rather than silently flattening them.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The abstraction intentionally covers non-streaming text chat only. It does not make provider capabilities identical; model capability negotiation and fallback are separate projects. Local test execution remains pending.
