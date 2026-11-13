from __future__ import annotations
from typing import Any

def generate_tool_specs(document: dict[str, Any], allowed_methods: set[str] | None = None) -> list[dict[str, Any]]:
    if not isinstance(document, dict) or not isinstance(document.get("paths"), dict):
        raise ValueError("OpenAPI document must contain a paths object")
    allowed = {m.lower() for m in (allowed_methods or {"get"})}
    specs = []
    for path, operations in document["paths"].items():
        if not isinstance(path, str) or not path.startswith("/") or ".." in path or not isinstance(operations, dict):
            continue
        for method, operation in operations.items():
            method = method.lower()
            if method not in allowed or not isinstance(operation, dict):
                continue
            operation_id = operation.get("operationId")
            if not isinstance(operation_id, str) or not operation_id.replace("_", "").isalnum():
                continue
            specs.append({"name": operation_id, "method": method.upper(), "path": path, "summary": str(operation.get("summary", ""))[:300]})
    if len({x["name"] for x in specs}) != len(specs):
        raise ValueError("duplicate operationId values")
    return specs
