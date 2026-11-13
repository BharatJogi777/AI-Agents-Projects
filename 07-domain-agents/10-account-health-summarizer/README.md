# Account health summarizer

Summarize supplied engagement, support and renewal signals into an explainable account health view.

## Safety and data boundaries

This project operates only on explicitly supplied inputs. It does not access or mutate customer accounts or CRM records, contact prospects, or make binding commercial decisions. Recommendations are explainable and require authorized human review.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## Limitations

Adapt scoring and policy rules to approved organizational criteria. Validate data provenance, consent, privacy, and applicable regulations before production use.
