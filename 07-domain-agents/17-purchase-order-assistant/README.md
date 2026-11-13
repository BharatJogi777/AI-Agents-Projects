# prepare_purchase_order

Purchase order assistant

## Safety and data boundaries

This tool processes only supplied records and configurable policy data. It does not submit purchase orders, award vendors, approve expenses, provide legal advice, sign contracts, or make payments. Outputs are drafts or review aids for authorized personnel.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## Limitations

Validate all policy thresholds, currency and tax treatment, contractual interpretations, evidence quality, and approval requirements with the responsible business or legal team.
