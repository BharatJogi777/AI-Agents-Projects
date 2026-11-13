from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Principal:
    subject: str
    tenant_id: str
    roles: frozenset[str]


def require_principal(principal: Principal | None) -> Principal:
    if principal is None or not principal.subject or not principal.tenant_id:
        raise PermissionError("authenticated tenant principal required")
    return principal


class TenantRepository:
    def __init__(self, records: list[dict[str, Any]]):
        self._records = records

    def list_for(self, principal: Principal | None, limit: int = 100) -> list[dict[str, Any]]:
        actor = require_principal(principal)
        if not 1 <= limit <= 500:
            raise ValueError("limit must be between 1 and 500")
        return [
            {"id": row["id"], "tenant_id": row["tenant_id"], "value": row["value"]}
            for row in self._records
            if row.get("tenant_id") == actor.tenant_id
        ][:limit]

    def get_for(self, principal: Principal | None, record_id: str) -> dict[str, Any]:
        actor = require_principal(principal)
        for row in self._records:
            if row.get("id") == record_id and row.get("tenant_id") == actor.tenant_id:
                return {"id": row["id"], "tenant_id": row["tenant_id"], "value": row["value"]}
        raise LookupError("record not found")
