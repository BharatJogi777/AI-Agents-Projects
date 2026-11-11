# Design notes

## Why an interface?

Tokenization is a model property, not a universal property of text. The planner accepts a TokenCounter so that an exact model-specific implementation can replace the heuristic without changing admission policy.

## Why whole-item admission?

Conversation turns, retrieved chunks, and tool results often have useful boundaries. Silently cutting arbitrary text can corrupt JSON, remove important qualifiers, or leave a partial tool transcript. This project drops an item as a whole and reports the decision. A later truncation project can implement explicit, content-aware strategies.

## Admission order

1. Mandatory items in caller-supplied order.
2. Optional items by descending priority, stable for ties.
3. Output in original caller-supplied order.

This means selection priority does not reorder the final prompt. The caller remains responsible for mapping item kinds into provider message roles and preserving any provider-specific ordering constraints.

## Failure policy

If mandatory items do not fit, planning fails with MandatoryContextOverflow. The caller must choose a recovery strategy; the planner does not silently drop system instructions or the current user request.
