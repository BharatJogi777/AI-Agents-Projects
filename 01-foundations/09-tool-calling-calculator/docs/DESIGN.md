# Design notes

## Trust boundaries

The model is an untrusted planner. It proposes a tool name and JSON arguments; application code validates and executes only the allowlisted `calculate` tool. Pydantic rejects extra fields and non-string expressions. Tool execution never uses model-generated Python.

## Arithmetic evaluator

The evaluator parses in Python expression mode and recursively accepts only numeric constants, selected binary operators, and unary plus/minus. All other AST nodes fail closed. Decimal arithmetic uses a local precision of 28 digits. Expression length, AST node count, exponent magnitude, numeric literal size, and result magnitude are bounded. Decimal arithmetic exceptions become controlled calculation errors.

## Tool loop

The agent preserves the assistant tool-call message and correlates each tool result with its call ID where supplied by the provider. Tool names are allowlisted; argument JSON must decode to an object; Pydantic rejects extra fields. A maximum model-step count, per-step tool-call count, request size, and final-answer size prevent unbounded work. Invalid tool calls become bounded failed tool results so the model can explain the failure.

## Provider adapter

The Ollama HTTP adapter owns a persistent HTTPX client unless one is injected. It enforces connect/request timeouts and sanitizes HTTP/provider errors. The CLI closes the client in a `finally` block. Provider/network retries are deliberately not mixed into the agent's tool loop.

## Operational boundaries

No eval, exec, imports, attribute lookup, arbitrary function calls, or shell execution are used. Tool results return to the model as data. Persistence, authentication, API hosting, streaming, rate limiting, multi-tenant isolation, and distributed tracing are out of scope for this CLI project.
