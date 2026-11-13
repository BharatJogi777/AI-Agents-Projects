# Customer support response drafter

Draft a customer reply from verified case facts and approved policy snippets without inventing resolutions.

## Safety and data boundaries

This project uses explicitly supplied records and policy inputs. It does not connect to customer accounts, disclose private order data, issue refunds, create shipping labels, or send messages. Outputs are drafts or screening decisions and require authorized human review.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## Limitations

Adapt rules to the organization's approved policies, privacy requirements, jurisdiction, and escalation procedures before use.
