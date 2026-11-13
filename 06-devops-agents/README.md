# DevOps, SRE, and Cloud Operations Agents

Investigate operational signals with read-only access by default. Any remediation must be narrowly scoped and approval-gated.

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


## Implemented projects (AG-251–AG-255)

| ID | Project | Implementation |
|---|---|---|
| AG-251 | Application log investigation agent | [01-application-log-investigation-agent](01-application-log-investigation-agent/) |
| AG-252 | Structured log anomaly explainer | [02-structured-log-anomaly-explainer](02-structured-log-anomaly-explainer/) |
| AG-253 | Trace investigation assistant | [03-trace-investigation-assistant](03-trace-investigation-assistant/) |
| AG-254 | Metrics query assistant | [04-metrics-query-assistant](04-metrics-query-assistant/) |
| AG-255 | Incident timeline builder | [05-incident-timeline-builder](05-incident-timeline-builder/) |


## Implemented projects (AG-256–AG-260)

| ID | Project | Implementation |
|---|---|---|
| AG-256 | Incident severity classifier | [06-incident-severity-classifier](06-incident-severity-classifier/) |
| AG-257 | On-call handoff summarizer | [07-on-call-handoff-summarizer](07-on-call-handoff-summarizer/) |
| AG-258 | Runbook retrieval assistant | [08-runbook-retrieval-assistant](08-runbook-retrieval-assistant/) |
| AG-259 | Runbook recommendation agent | [09-runbook-recommendation-agent](09-runbook-recommendation-agent/) |
| AG-260 | Kubernetes pod diagnosis agent | [10-kubernetes-pod-diagnosis-agent](10-kubernetes-pod-diagnosis-agent/) |


## Implemented projects (AG-261–AG-265)

| ID | Project | Implementation |
|---|---|---|
| AG-261 | Kubernetes event explainer | [11-kubernetes-event-explainer](11-kubernetes-event-explainer/) |
| AG-262 | Kubernetes deployment reviewer | [12-kubernetes-deployment-reviewer](12-kubernetes-deployment-reviewer/) |
| AG-263 | Kubernetes resource advisor | [13-kubernetes-resource-advisor](13-kubernetes-resource-advisor/) |
| AG-264 | Kubernetes capacity planner | [14-kubernetes-capacity-planner](14-kubernetes-capacity-planner/) |
| AG-265 | Kubernetes manifest security reviewer | [15-kubernetes-manifest-security-reviewer](15-kubernetes-manifest-security-reviewer/) |
