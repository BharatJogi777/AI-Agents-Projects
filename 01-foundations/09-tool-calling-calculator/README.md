# AG-009 — Tool-calling calculator

**Status:** Modular implementation expanded; tests are authored but not locally executed.  
**Runtime:** Python 3.12+ · **Model:** Ollama `qwen3:4b` by default

## Purpose

The LLM interprets the natural-language request and chooses the calculator tool. Python validates the tool arguments and evaluates arithmetic deterministically. The application never executes model-generated Python, `eval()`, shell commands, or arbitrary AST nodes.

## Architecture

```text
Natural-language request
        |
        v
CalculatorAgent (bounded model/tool loop)
        |
        v
OllamaChatClient ----> Ollama /api/chat
        |
        | tool call (structured JSON)
        v
tools.execute_tool (allowlist + Pydantic)
        |
        v
arithmetic.calculate (restricted AST + Decimal)
        |
        v
tool result -> model -> final answer
```

## Modules

- `calculator_core/arithmetic.py`: parser, AST allowlist, Decimal arithmetic, numeric/expression limits.
- `calculator_core/tools.py`: strict argument schema, tool definition, allowlisted dispatch.
- `calculator_core/agent.py`: bounded orchestration and tool-result messages.
- `calculator_core/provider.py`: reusable HTTP client and Ollama response/error handling.
- `app.py`: compatibility exports for existing examples/tests.
- `main.py`: CLI composition root.

## Setup and run

```bash
ollama pull qwen3:4b
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python main.py "What is (19 + 23) multiplied by 2?"
pytest
```

## Safety properties

- Only arithmetic literals, unary signs, and selected binary operators are accepted.
- Expression length and AST node count are bounded.
- Exponents are restricted to integers from -8 through 8.
- Numeric values and results are bounded; Decimal avoids common binary floating-point surprises.
- Tool names are allowlisted and argument fields are strict.
- Model steps are bounded; provider errors are sanitized.

## Tests

`pytest` runs arithmetic, malicious-expression rejection, tool dispatch, agent-loop, and provider-adapter tests without a live Ollama server. The tests are committed but have not been executed in the maintainer's environment.

## Limitations

This is a single-process CLI example. It has no API authentication, persistent run history, per-user quotas, or distributed tracing. Add those only when turning it into a hosted service.
