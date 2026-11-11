# Design notes

The model is an untrusted planner. It proposes a tool name and JSON arguments; application code validates and executes only the allowlisted calculate tool. Pydantic rejects extra fields and non-string expressions.

The evaluator parses in Python expression mode and recursively accepts only numeric constants, selected binary operators, and unary plus/minus. All other AST nodes fail closed. Decimal arithmetic uses a local precision of 28 digits. Expression length, AST node count, exponent magnitude, and result magnitude are bounded.

No eval, exec, imports, attribute lookup, or arbitrary function calls are used. Tool results return to the model as data. A maximum step count prevents unbounded loops. Provider and HTTP errors propagate to the caller; invalid tool calls become bounded failed tool results.

Persistence, authentication, API hosting, streaming, rate limiting, and multi-tenant isolation are intentionally out of scope.
