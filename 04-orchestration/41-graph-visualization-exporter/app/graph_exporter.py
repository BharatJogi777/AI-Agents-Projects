"""Export validated workflow graphs to Graphviz DOT without external dependencies."""
from dataclasses import dataclass, field
from typing import Iterable

@dataclass(frozen=True)
class Node:
    id: str
    label: str = ""
    kind: str = "task"

@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    label: str = ""

@dataclass
class WorkflowGraph:
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)

    def validate(self) -> None:
        ids = [n.id for n in self.nodes]
        if any(not x or not x.replace("_", "").replace("-", "").isalnum() for x in ids):
            raise ValueError("node ids must be non-empty alphanumeric identifiers")
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate node id")
        known = set(ids)
        for edge in self.edges:
            if edge.source not in known or edge.target not in known:
                raise ValueError(f"edge references unknown node: {edge}")

    def to_dot(self) -> str:
        self.validate()
        lines = ["digraph workflow {", "  rankdir=LR;"]
        for node in self.nodes:
            label = _quote(node.label or node.id)
            shape = "diamond" if node.kind == "condition" else "box"
            lines.append(f'  "{node.id}" [label="{label}", shape={shape}];')
        for edge in self.edges:
            suffix = f' [label="{_quote(edge.label)}"]' if edge.label else ""
            lines.append(f'  "{edge.source}" -> "{edge.target}"{suffix};')
        lines.append("}")
        return "\n".join(lines) + "\n"

def _quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
