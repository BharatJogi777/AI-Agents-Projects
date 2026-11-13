# Clinical document summarization with review

Prepares a structured, source-linked review packet from supplied clinical document metadata. This implementation deliberately does not generate a clinical summary or interpret findings.

## Safety boundaries

- Administrative workflow support only; no diagnosis, treatment recommendation, or patient-facing advice.
- Source references and clinician review are mandatory.
- No external EHR integration or automatic document submission.

## Run tests

```bash
python -m pytest
```
