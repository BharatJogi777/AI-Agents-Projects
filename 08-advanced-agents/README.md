# Advanced Interfaces and Autonomous Workflows

Explore advanced interaction modes and durable workflows while preserving clear user control and safe interruption.

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


## Implemented project batch: AG-351–AG-355

| ID | Project | Catalogue status |
|---|---|---|
| AG-351 | [Browser research assistant](./01-browser-research-assistant/) | In progress |
| AG-352 | [Browser form-filling assistant with approval](./02-browser-form-filling-assistant-with-approval/) | In progress |
| AG-353 | [Browser navigation state tracker](./03-browser-navigation-state-tracker/) | In progress |
| AG-354 | [Web page change monitor](./04-web-page-change-monitor/) | In progress |
| AG-355 | [Multi-site comparison agent](./05-multi-site-comparison-agent/) | In progress |


## Implemented project batch: AG-356–AG-360

| ID | Project | Catalogue status |
|---|---|---|
| AG-356 | [Accessible browser interaction assistant](./06-accessible-browser-interaction-assistant/) | In progress |
| AG-357 | [Screenshot-to-UI explanation agent](./07-screenshot-to-ui-explanation-agent/) | In progress |
| AG-358 | [Visual UI regression investigator](./08-visual-ui-regression-investigator/) | In progress |
| AG-359 | [Voice conversation agent](./09-voice-conversation-agent/) | In progress |
| AG-360 | [Speech transcription task agent](./10-speech-transcription-task-agent/) | In progress |


## Implemented project batch: AG-361–AG-365

| ID | Project | Catalogue status |
|---|---|---|
| AG-361 | [Voice command intent router](./11-voice-command-intent-router/) | In progress |
| AG-362 | [Text-to-speech response agent](./12-text-to-speech-response-agent/) | In progress |
| AG-363 | [Meeting audio summarizer](./13-meeting-audio-summarizer/) | In progress |
| AG-364 | [Call quality analysis assistant](./14-call-quality-analysis-assistant/) | In progress |
| AG-365 | [Image understanding assistant](./15-image-understanding-assistant/) | In progress |


## Implemented project batch: AG-366–AG-370

| ID | Project | Catalogue status |
|---|---|---|
| AG-366 | [Chart and diagram interpreter](./16-chart-and-diagram-interpreter/) | In progress |
| AG-367 | [Receipt image extraction agent](./17-receipt-image-extraction-agent/) | In progress |
| AG-368 | [Product image catalog assistant](./18-product-image-catalog-assistant/) | In progress |
| AG-369 | [Video chapter summarizer](./19-video-chapter-summarizer/) | In progress |
| AG-370 | [Video event timeline assistant](./20-video-event-timeline-assistant/) | In progress |

## Projects 21–25

| ID | Project | Implementation |
|---|---|---|
| AG-371 | Multimodal Document Assistant | [21-multimodal-document-assistant](./21-multimodal-document-assistant/) |
| AG-372 | Audio Video Meeting Assistant | [22-audio-video-meeting-assistant](./22-audio-video-meeting-assistant/) |
| AG-373 | Event Triggered Inbox Agent | [23-event-triggered-inbox-agent](./23-event-triggered-inbox-agent/) |
| AG-374 | Scheduled Report Generation Agent | [24-scheduled-report-generation-agent](./24-scheduled-report-generation-agent/) |
| AG-375 | Webhook Triggered Workflow Agent | [25-webhook-triggered-workflow-agent](./25-webhook-triggered-workflow-agent/) |

## Projects 26–30

| ID | Project | Implementation |
|---|---|---|
| AG-376 | Email Event Triage Agent | [26-email-event-triage-agent](./26-email-event-triage-agent/) |
| AG-377 | Long Running Research Agent | [27-long-running-research-agent](./27-long-running-research-agent/) |
| AG-378 | Long Running Workflow Monitor | [28-long-running-workflow-monitor](./28-long-running-workflow-monitor/) |
| AG-379 | Background Task Progress Reporter | [29-background-task-progress-reporter](./29-background-task-progress-reporter/) |
| AG-380 | Human Takeover Browser Workflow | [30-human-takeover-browser-workflow](./30-human-takeover-browser-workflow/) |
