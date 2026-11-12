# AG-048 — Agent trace event emitter

Emits ordered, structured lifecycle events with run correlation, sequence numbers, UTC timestamps, bounded attributes, and common sensitive-field redaction.

```python
events=[]
trace=TraceEmitter("run-42",events.append)
trace.emit("agent.started",{"model":"qwen3:4b"})
trace.emit("tool.completed",{"tool":"search","api_key":"redacted"})
```

The sink is injected (in-memory list in the example; use an OpenTelemetry exporter or queue in production). Sink calls are serialized per emitter. A failed sink call consumes its sequence number to avoid reusing an identifier after an uncertain partial write. This is not a complete OpenTelemetry SDK and does not guarantee durable delivery.

Test: `python -m pip install pytest && pytest`.
