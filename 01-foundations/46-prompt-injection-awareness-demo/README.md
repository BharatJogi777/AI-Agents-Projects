# AG-046 — Prompt injection awareness demo

Demonstrates trust separation between application policy, user input, and retrieved documents. The builder labels untrusted sections and enforces a total character budget. The action policy independently enforces a server-side allowlist and optional approval requirement.

```python
from prompt_security import PromptBuilder,PromptParts,ActionPolicy
prompt=PromptBuilder().build(PromptParts("Only search public docs","Find deployment guide","Retrieved page text"))
policy=ActionPolicy({"search_docs","send_email"},{"send_email"})
decision=policy.evaluate("send_email",approved=False)
```

**Security warning:** delimiters and prompt wording are defense-in-depth, not prompt-injection prevention. Never let model output authorize tools. Validate action names/arguments in application code, scope credentials, isolate retrieved content, and require authenticated human approval for consequential actions. Tests cover the deterministic policy boundary, not model robustness.

Test: `python -m pip install pytest && pytest`.
