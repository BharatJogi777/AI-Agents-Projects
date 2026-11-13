# DNS failure investigator

Evaluate supplied DNS query observations for NXDOMAIN, SERVFAIL, timeout, and inconsistent answers.

## Safety boundary

This project analyzes caller-supplied diagnostic data only. It does not connect to cloud accounts, databases, DNS resolvers, or load balancers and performs no remediation.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## Limitations

Results depend on the completeness and correctness of the supplied snapshot. Treat findings as triage guidance; validate with authoritative telemetry and operational runbooks before taking action.
