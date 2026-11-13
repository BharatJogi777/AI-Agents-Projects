"""Read-only sample order repository.

Replace this adapter with an authorized database/API implementation in production.
"""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrderRecord:
    order_id: str
    status: str
    item_count: int
    currency: str


_ORDERS: dict[str, OrderRecord] = {
    "ORD-1001": OrderRecord("ORD-1001", "processing", 3, "INR"),
    "ORD-1002": OrderRecord("ORD-1002", "shipped", 1, "INR"),
}


class OrderNotFoundError(LookupError):
    """Raised when the requested order does not exist."""


class InMemoryOrderRepository:
    """Minimal read-only repository backed by immutable records."""

    def get(self, order_id: str) -> OrderRecord:
        try:
            return _ORDERS[order_id]
        except KeyError as exc:
            raise OrderNotFoundError(f"Order '{order_id}' was not found") from exc
