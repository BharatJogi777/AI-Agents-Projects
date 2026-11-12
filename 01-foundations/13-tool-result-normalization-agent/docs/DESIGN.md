# Design notes — AG-013

## Boundary and data contract

Tool handlers may return values that are not directly suitable for an LLM provider request. The normalizer converts a restricted set of common values into a JSON-compatible envelope:

```json
{"ok": true, "data": {"status": "ready"}, "warnings": []}
```

The `ok` field is a strict boolean. Tool errors should be represented by the caller using `ok=false`; exception text and stack traces should not be passed into this function as user-facing data.

## Safe traversal

Supported values include null, booleans, bounded integers, finite floats, strings, dates, datetimes, finite Decimals, UUIDs, bytes metadata, and built-in dict/list/tuple containers. Unsupported objects are represented by type metadata. The implementation does not call arbitrary `repr()`, `str()`, mapping protocols, or custom JSON encoders.

An active recursion-path set detects true cycles while allowing the same non-cyclic object to appear in multiple branches. Container depth, item counts, string lengths, and warning counts are bounded.

## Redaction

Sensitive keys are normalized case-insensitively and with separators removed, then matched against a conservative built-in key set. Values under matching keys are replaced before recursive traversal. This avoids accidentally processing or serializing a credential value.

Key-based redaction is not secret detection. It cannot reliably identify secrets embedded in arbitrary prose, unknown field names, or encoded payloads. Callers should minimize sensitive tool output and add domain-specific filtering.

## Output budget

The complete envelope is serialized as UTF-8 JSON and measured in bytes. If it exceeds the configured budget, the original data is replaced with a small omission marker and a warning. The normalizer never slices serialized JSON, which could produce malformed output.

## Integration and non-goals

Call this utility after a tool handler returns and before appending the tool result to an LLM conversation. The agent loop remains responsible for tool-call IDs, retry budgets, provider message shape, and conversation context limits. This package does not provide authorization, sandboxing, or execution timeouts.
