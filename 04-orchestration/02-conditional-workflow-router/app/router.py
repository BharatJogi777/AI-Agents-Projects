from dataclasses import dataclass
from typing import Any, Callable

Predicate = Callable[[dict[str, Any]], bool]
Handler = Callable[[dict[str, Any]], dict[str, Any]]

@dataclass(frozen=True)
class Route:
    name: str
    predicate: Predicate
    handler: Handler

class ConditionalRouter:
    def __init__(self, routes: list[Route], default: Handler | None = None):
        names = [route.name for route in routes]
        if len(names) != len(set(names)) or any(not n.strip() for n in names):
            raise ValueError("route names must be unique and non-empty")
        self.routes, self.default = tuple(routes), default

    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        snapshot = dict(state)
        for route in self.routes:
            if route.predicate(snapshot):
                result = route.handler(snapshot)
                if not isinstance(result, dict):
                    raise TypeError(f"route {route.name} must return a dictionary")
                return {"route": route.name, "state": {**snapshot, **result}}
        if self.default is None:
            raise LookupError("no route matched and no default handler is configured")
        result = self.default(snapshot)
        if not isinstance(result, dict):
            raise TypeError("default handler must return a dictionary")
        return {"route": "default", "state": {**snapshot, **result}}
