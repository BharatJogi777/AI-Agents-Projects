"""Dependency-aware task scheduler with cycle detection."""
from dataclasses import dataclass, field

@dataclass
class DependencyScheduler:
    dependencies: dict[str, set[str]] = field(default_factory=dict)

    def add(self, task_id: str, depends_on: set[str] | None = None) -> None:
        if not task_id or task_id in self.dependencies:
            raise ValueError("task ID must be non-empty and unique")
        deps = set(depends_on or ())
        if task_id in deps:
            raise ValueError("task cannot depend on itself")
        self.dependencies[task_id] = deps

    def order(self) -> list[str]:
        unknown = {d for deps in self.dependencies.values() for d in deps} - self.dependencies.keys()
        if unknown:
            raise ValueError(f"unknown dependencies: {sorted(unknown)}")
        remaining = {k: set(v) for k, v in self.dependencies.items()}
        ordered: list[str] = []
        while remaining:
            ready = sorted(k for k, deps in remaining.items() if not deps)
            if not ready:
                raise RuntimeError("dependency cycle detected")
            for task in ready:
                ordered.append(task)
                remaining.pop(task)
            for deps in remaining.values():
                deps.difference_update(ready)
        return ordered

    def ready(self, completed: set[str]) -> list[str]:
        unknown = completed - self.dependencies.keys()
        if unknown:
            raise ValueError(f"unknown completed tasks: {sorted(unknown)}")
        return sorted(task for task, deps in self.dependencies.items()
                      if task not in completed and deps <= completed)
