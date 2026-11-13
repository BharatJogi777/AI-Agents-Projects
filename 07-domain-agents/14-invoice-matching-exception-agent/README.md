# Invoice matching exception agent

Compare invoice and purchase-order records using configurable amount tolerance and explicit exception reasons.

## Safety and data boundaries

These tools process only explicitly supplied text or structured records. They do not connect to customer systems, create accounting entries, approve invoices, or initiate payments. Extracted and classified information is provisional and should be reviewed against original source documents.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## Limitations

Keyword classification and regular-expression extraction are deterministic baselines, not substitutes for domain validation, OCR quality checks, accounting controls, or human review.
