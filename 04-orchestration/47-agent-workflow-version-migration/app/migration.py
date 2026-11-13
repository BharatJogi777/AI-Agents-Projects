"""Migrate persisted workflow state between explicit schema versions."""
from dataclasses import dataclass
from typing import Any, Callable

Migration = Callable[[dict[str, Any]], dict[str, Any]]

@dataclass
class MigrationRegistry:
    migrations: dict[tuple[int, int], Migration]

    def migrate(self, state: dict[str, Any], source: int, target: int) -> dict[str, Any]:
        if source < 1 or target < source:
            raise ValueError("versions must be positive and target >= source")
        current = dict(state)
        version = source
        while version < target:
            step = self.migrations.get((version, version + 1))
            if step is None:
                raise LookupError(f"missing migration {version} -> {version + 1}")
            updated = step(dict(current))
            if not isinstance(updated, dict):
                raise TypeError("migration must return a dictionary")
            current = updated
            version += 1
        return current
