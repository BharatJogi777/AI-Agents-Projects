# Design notes

## Counting is separate from policy

A token counter implements one method: count a string for a particular tokenizer. The planner only consumes that contract. This lets tests use deterministic counts, local demos use a heuristic, and production adapters use a tokenizer matching the target model.

## Why heuristic counts are not production-safe

A fixed characters-per-token ratio cannot accurately represent different languages, code, JSON, punctuation, or tokenizer versions. It is included only to make the example runnable without model SDKs or network access.

## Why reserve output tokens?

The context window is shared by the input and generated output. The planner therefore subtracts output reserve and safety margin before admitting prompt content. The reserve is not part of the input plan.

## Why atomic context items?

A retrieval chunk, tool result, or conversation turn has a semantic boundary. Arbitrary truncation can break JSON, remove qualifiers, or corrupt a tool-call/result pair. This project drops whole items and reports each decision. AG-006 implements explicit truncation strategies.

## Greedy priority policy

Mandatory items are considered first in input order. Optional items are considered by descending priority with stable tie ordering. If a high-priority item is too large, it is dropped and later smaller items may still fit. This is deterministic and explainable; it is not a globally optimal knapsack solver.

## Provider-specific framing

Counting text alone does not count chat-message wrappers, tool schemas, images, audio, or provider metadata. A real integration should account for these separately and validate estimates against provider-reported usage.
