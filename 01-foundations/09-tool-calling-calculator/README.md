# AG-009 — Tool-calling calculator

**Status:** In progress — code and tests committed; local execution pending.  
**Model:** Ollama /api/chat; default qwen3:4b.

The model converts a natural-language request into a calculate tool call. Python validates the arguments and evaluates the expression using a restricted AST parser and Decimal arithmetic. The model does not calculate mentally, and Python never executes model-generated Python code.

## Supported arithmetic

Numbers, parentheses, unary plus/minus, addition, subtraction, multiplication, division, floor division, modulo, and integer powers from -8 to 8. Expression length, AST complexity, and result magnitude are bounded. Names, function calls, attribute access, comparisons, imports, and eval/exec are rejected.

## Setup and run

Requires Python 3.12+ and Ollama running on the host.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
ollama pull qwen3:4b
```

Run the CLI with: python -m main \"What is 19 plus 23?\". Set OLLAMA_BASE_URL and OLLAMA_MODEL to override the defaults.

## Tests

Run pytest. Tests use a fake model client and do not require Ollama. They cover arithmetic, unsafe expressions, tool dispatch, schema validation, and step limits.

## Safety

Only the calculate tool is exposed. No shell, filesystem, network, or database tools exist. The evaluator never calls eval or exec. This is a teaching CLI foundation, not a multi-tenant service. Model tool-call compatibility varies by Ollama model.
