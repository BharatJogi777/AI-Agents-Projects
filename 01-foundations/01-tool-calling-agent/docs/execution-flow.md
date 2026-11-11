# Execution flow walkthrough

Run: python -m app.main "What is 19 plus 23? Use a tool to calculate it."

1. main.py reads the prompt and creates settings.
2. OllamaChatClient sends conversation and tool definitions to Ollama.
3. Model may return a tool_calls array naming add_numbers with JSON arguments.
4. ToolCallingAgent passes the name and object to execute_tool.
5. execute_tool rejects names outside its dictionary and validates arguments.
6. add_numbers computes the sum in ordinary Python.
7. Agent appends a role=tool message containing the result.
8. Ollama receives the updated conversation and writes the final answer.

A tool call is not Python code. It is structured data interpreted by the application under its allowlist.

## Debugging

- If the model returns text instead of a tool call, inspect model tool-calling support.
- If Ollama is unreachable, check the service, base URL, and installed model.
- If a tool is rejected, compare its exact name and JSON arguments with app/tools.py.
- Run fake-client unit tests before testing the local model.
