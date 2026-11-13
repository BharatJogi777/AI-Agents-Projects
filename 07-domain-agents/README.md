# Business and Industry Domain Agents

Support a domain workflow with traceable inputs, policy boundaries, and human review for consequential decisions.

## Catalogue scope

This track contains 50 project specifications in the root [project catalogue](../docs/PROJECT_CATALOG.md) and machine-readable [JSON catalogue](../catalogue/projects.json). Catalogue entries are not claims of completed implementations.

## Implementation expectations

- Give every project a standalone purpose, explicit inputs and outputs, and a reproducible local run path.
- Keep model calls behind a small adapter; keep validation, permissions, and side effects in deterministic code.
- Add unit tests for normal behavior and important failure paths.
- Document model requirements, resource usage, limitations, and safety boundaries.
- Use the maturity labels in [PROJECT_STANDARD.md](../docs/PROJECT_STANDARD.md).

## Project status

Projects are implemented in priority order. Check the catalogue for current status; do not infer status from a folder existing.


## Implemented projects (AG-301–AG-305)

| ID | Project | Implementation |
|---|---|---|
| AG-301 | Customer support triage agent | [01-customer-support-triage-agent](01-customer-support-triage-agent/) |
| AG-302 | Customer support response drafter | [02-customer-support-response-drafter](02-customer-support-response-drafter/) |
| AG-303 | Order status assistant | [03-order-status-assistant](03-order-status-assistant/) |
| AG-304 | Refund eligibility checker | [04-refund-eligibility-checker](04-refund-eligibility-checker/) |
| AG-305 | Returns workflow assistant | [05-returns-workflow-assistant](05-returns-workflow-assistant/) |


## Implemented projects (AG-306–AG-310)

| ID | Project | Implementation |
|---|---|---|
| AG-306 | Subscription cancellation assistant | [06-subscription-cancellation-assistant](06-subscription-cancellation-assistant/) |
| AG-307 | Sales lead qualification agent | [07-sales-lead-qualification-agent](07-sales-lead-qualification-agent/) |
| AG-308 | Sales call preparation assistant | [08-sales-call-preparation-assistant](08-sales-call-preparation-assistant/) |
| AG-309 | CRM data enrichment agent | [09-crm-data-enrichment-agent](09-crm-data-enrichment-agent/) |
| AG-310 | Account health summarizer | [10-account-health-summarizer](10-account-health-summarizer/) |
