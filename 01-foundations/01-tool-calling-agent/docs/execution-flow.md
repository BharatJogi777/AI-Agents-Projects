# Execution flow walkthrough

Run:

```bash
python -m app.main "What is 19 plus 23? Use a tool to calculate it."
```

1. `main.py` reads the prompt and creates validated settings.
2. `OllamaChatClient` sends the conversation and tool definitions to Ollama's OpenAI-compatible endpoint.
3. The model may return a `tool_calls` array naming `add_numbers` with JSON arguments.
4. `ToolCallingAgent` validates the call envelope, ID, argument size, and JSON object shape.
5. `execute_tool` rejects names outside its local allowlist and validates arguments with Pydantic.
6. `add_numbers` computes the sum in ordinary Python.
7. The agent appends a `role=tool` message containing the bounded result.
8. Ollama receives the updated conversation and writes the final answer.
9. The loop stops on a final answer or raises after the configured step budget.

A tool call is not Python code. It is structured data interpreted by the application under its allowlist.

## HTTP health checks

- `GET /health/live`: process-only liveness; no dependency call.
- `GET /health/ready`: verifies Ollama is reachable and the configured model is listed.
- `POST /v1/agent/run`: executes the bounded agent loop.

## Debugging

- If the model returns text instead of a tool call, inspect model tool-calling support.
- If Ollama is unreachable, check the service, base URL, and installed model.
- If readiness is 503, call `ollama list` and compare the exact model name with `OLLAMA_MODEL`.
- If a tool is rejected, compare its exact name and JSON arguments with `app/tools.py`.
- Run fake-client unit tests before testing the local model.
