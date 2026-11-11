# Threat model

## Assets

- Application-owned system and developer instructions.
- Credentials and private operational data that may be available to a larger agent.
- Tool permissions and external side effects.

## Trust boundaries

| Input | Trust level | Required treatment |
|---|---|---|
| System/developer policy | Trusted application configuration | Code-owned, reviewed, immutable at request time |
| User message | Untrusted | Validate size and shape; never interpret as policy |
| Retrieved content | Untrusted | Treat as data; preserve source/provenance |
| Tool output | Untrusted | Validate before reuse; never grant new permissions |

## Threats and controls

- **Instruction override:** keep policy separate from user content; independently enforce tool permissions.
- **Markup breakout:** escape user-controlled markup in the demonstration framing.
- **Oversized input:** enforce a configurable character limit before model invocation.
- **Provider role mismatch:** use an explicit adapter and test the resulting role mapping.
- **Tool misuse:** do not infer authorization from model output; check permissions in deterministic code.

## Residual risk

A model can still follow malicious instructions embedded in user or retrieved content. This demo does not eliminate prompt injection. For consequential actions, use least-privilege tools, deterministic policy checks, approval gates, and adversarial evaluations.
