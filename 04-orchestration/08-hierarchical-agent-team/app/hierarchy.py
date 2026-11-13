from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass(frozen=True)
class AgentNode:
    id: str
    worker: str | None = None
    children: tuple["AgentNode", ...] = ()

class HierarchicalTeam:
    def __init__(self, workers: dict[str, Callable[[list[Any]], Any]], max_depth: int = 4, max_nodes: int = 50):
        if max_depth < 1 or max_nodes < 1: raise ValueError("limits must be positive")
        self.workers, self.max_depth, self.max_nodes = dict(workers), max_depth, max_nodes

    def run(self, root: AgentNode) -> Any:
        count = 0
        seen: set[int] = set()
        def visit(node: AgentNode, depth: int) -> Any:
            nonlocal count
            if depth > self.max_depth: raise ValueError("delegation depth exceeded")
            if id(node) in seen: raise ValueError("cycle or reused node detected")
            seen.add(id(node)); count += 1
            if count > self.max_nodes: raise ValueError("node budget exceeded")
            if not node.id.strip(): raise ValueError("node id is required")
            if node.children and node.worker: raise ValueError("node cannot be both manager and worker")
            values = [visit(child, depth + 1) for child in node.children]
            if node.worker is None:
                if not values: raise ValueError("manager node must have children")
                return {"manager": node.id, "results": values}
            handler = self.workers.get(node.worker)
            if handler is None: raise ValueError(f"unknown worker: {node.worker}")
            return handler(values)
        return visit(root, 1)
