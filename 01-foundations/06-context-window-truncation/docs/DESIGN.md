# Design notes

## Context selection policy

System messages and the pending current user request are mandatory. Completed turns are considered newest-first and admitted as a contiguous suffix. The first turn that does not fit stops selection; older turns are not cherry-picked. This avoids creating misleading gaps in conversational history.

## Atomic tool exchanges

A completed turn can contain assistant tool-call messages, their matching tool results, and a final assistant response. Tool call IDs are validated and every result must match a pending call. The entire turn is retained or dropped. The truncator never cuts a tool result in the middle, never leaves an assistant tool call without its result, and never leaves a tool result without its call.

Large tool results therefore cause their containing turn to be dropped if the whole turn cannot fit. A separate bounded-output or structured summarization stage can reduce them before planning. Arbitrarily slicing JSON or provider payloads here would risk corrupting data and tool protocol state.

## Token accounting

The counter is injected through a protocol. The heuristic counter is only for examples. The optional tiktoken adapter supports known model encodings; for other providers use their official tokenizer or token-count API. Message framing overhead is configurable, but provider-specific serialization, tool schemas, image/audio payloads, and hidden metadata may cost additional tokens. For hard limits, count the fully serialized request or use provider accounting where available.

## Failure behavior

If mandatory context exceeds the available input budget, the planner raises MandatoryContextTooLarge. It never silently drops system instructions or the current request. Invalid/incomplete turns fail validation before selection. The returned estimated token count is recomputed from retained messages and cannot exceed the configured input budget under the injected counter.
