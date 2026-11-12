# AG-050 — FastAPI agent endpoint

Exposes an injected callable through a typed HTTP boundary. Includes strict Pydantic request validation, a 4,000-character prompt limit, liveness/readiness endpoints, and sanitized execution failures.

```python
from fastapi import FastAPI
from agent_api import create_app
def agent(prompt: str) -> str:
    return "Agent answer: " + prompt
app: FastAPI = create_app(agent)
```

Run with `uvicorn app:app --host 0.0.0.0 --port 8000`. Replace the demo callable with a real agent service. For production, run blocking model/tool calls in a worker thread or queue; add authentication, rate limits, request IDs, tracing, and a durable run registry. Readiness here means the API process is initialized, not that an external model is reachable.

Test: `python -m pip install 'fastapi>=0.110' 'httpx>=0.27' pytest && pytest`.
