# Design notes

## Why stop at the first turn that does not fit?

The selected turns form a contiguous suffix of conversation history. Skipping an oversized recent turn to retain older messages can create confusing context gaps. A future policy may support explicit importance ranking, but it must document that semantic trade-off.

## Why whole turns?

A user message without its answer, or an answer without its question, can misrepresent the conversation. The implementation therefore groups exactly one user and one assistant message by turn ID and admits or drops the pair atomically.

## Why preserve the current user message?

The current request defines the task the model must answer. If it cannot fit alongside the system instructions, the request should fail visibly so an upstream layer can handle it.

## Extension points

A production message schema should model assistant tool calls, tool results, images/audio, provider metadata, and per-message trust labels. Count the serialized provider request or use the provider's token-counting API when possible. Never assume message text alone represents the full request cost.
