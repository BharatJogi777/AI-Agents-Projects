# AG-131 — Email drafting MCP server

A deterministic draft builder that validates subject, body, and recipient addresses. It deliberately does not send email.

## Run
```bash
pip install -e '.[dev]'
pytest
```

Expose draft creation as a tool that returns a preview requiring human review. Sending must be a separate capability with explicit user confirmation, recipient allowlists, audit records, and idempotency. Never infer or invent recipient addresses from untrusted context.

## Limitations
The email validation is syntactic only; it does not prove mailbox ownership or deliverability. No SMTP/API integration is included.
