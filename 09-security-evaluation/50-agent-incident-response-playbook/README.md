# Agent incident response playbook

**Project ID:** AG-450

Generate structured containment and investigation checklists for common agent incidents. The library does not perform containment, change permissions, rotate credentials, or contact responders.

## Run
```bash
pip install -e '.[test]'
pytest
```

## Limitations
Adapt steps to your incident command structure, regulatory obligations, and service architecture. A generated checklist is not a substitute for an approved incident response plan.