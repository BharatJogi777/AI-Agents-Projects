from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class ToolRequest:
    name: str
    arguments: dict[str, Any]

@dataclass(frozen=True)
class ToolResult:
    tool: str
    output: Any
    next_tool: str | None = None

class ToolRouterGraph:
    def __init__(self, tools: dict[str, Callable[[dict[str, Any]], ToolResult]], max_hops: int = 5):
        if not tools or max_hops < 1: raise ValueError("tools and positive hop limit required")
        self.tools, self.max_hops = dict(tools), max_hops

    def run(self, first: ToolRequest) -> list[ToolResult]:
        current, results = first, []
        for _ in range(self.max_hops):
            handler = self.tools.get(current.name)
            if handler is None: raise ValueError(f"tool not allowed: {current.name}")
            if not isinstance(current.arguments, dict): raise TypeError("tool arguments must be an object")
            result = handler(dict(current.arguments))
            if not isinstance(result, ToolResult) or result.tool != current.name:
                raise TypeError("tool returned invalid result")
            results.append(result)
            if result.next_tool is None: return results
            current = ToolRequest(result.next_tool, {"previous": result.output})
        raise RuntimeError("maximum tool hops exceeded")
