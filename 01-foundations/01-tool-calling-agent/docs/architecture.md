# Architecture

| Component | Responsibility | Must not do |
|---|---|---|
| API / CLI | Accept input and return output | Decide which tools are trusted |
| ToolCallingAgent | Own the bounded model/tool loop | Execute arbitrary model-provided code |
| ChatClient protocol | Define provider boundary | Contain business tool implementations |
| OllamaChatClient | Translate messages to Ollama HTTP | Authorize tool use |
| Tool registry | Dispatch allowlisted functions | Dynamically import model-selected modules |
| Pydantic models | Validate tool arguments | Treat valid input as authorized intent |

## Request lifecycle

1. CLI/API validates the user prompt.
2. Agent builds a conversation with trusted system instructions.
3. Model receives registered tool schemas.
4. Proposed tool name is looked up in the local allowlist.
5. Pydantic validates arguments before execution.
6. Deterministic Python handler returns a result.
7. Result is appended as a tool message.
8. Model produces a final response or the step budget is exhausted.

The model proposes actions. Python owns validation, authorization, execution, and limits.

## Trust boundaries

User input, model output, and tool output are untrusted. The local allowlist is the authority for executable capabilities. Dependency injection lets tests replace the provider with a deterministic fake.
