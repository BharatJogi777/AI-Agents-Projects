# AG-047 — Untrusted tool-output handling

Normalizes arbitrary tool results into a bounded envelope labeled `untrusted`. It recursively redacts common credential fields, handles circular/unsupported values, caps nesting/collection size, and reports truncation.

```python
from tool_output import ToolOutputNormalizer
envelope=ToolOutputNormalizer(max_chars=4000).normalize(
    "ticket_search", {"items":[{"title":"Incident","api_key":"never forward"}]})
# Pass envelope.content to the model only as untrusted data.
```

This handles common structured secret fields, not every secret embedded in free text. Apply provider-specific secret scanning/DLP where required; never return raw tool exceptions or credentials to the model. Tool output remains untrusted even after normalization.

Test: `python -m pip install pytest && pytest`.
