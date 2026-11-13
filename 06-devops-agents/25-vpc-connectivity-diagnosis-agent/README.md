# VPC connectivity diagnosis agent

Trace a reported network path across route, security-group, network-ACL, and endpoint evidence to identify likely blockers.

## Safety boundary

Analyzes supplied snapshots only. It does not connect to AWS or change network configuration. Verify findings against live state and approved network architecture.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## Limitations

This deterministic path checker depends on accurate caller-supplied evidence. It does not evaluate every AWS routing, DNS, firewall, peering, transit-gateway, or service-specific behavior.
