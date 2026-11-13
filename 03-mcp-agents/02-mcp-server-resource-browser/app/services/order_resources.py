"""Application service for rendering order resources."""
import json
import re

from app.repositories.orders import InMemoryOrderRepository

_ORDER_ID = re.compile(r"^ORD-[0-9]{4}$")


class InvalidResourceURIError(ValueError):
    """Raised when a resource URI contains an invalid order identifier."""


class OrderResourceService:
    def __init__(self, repository: InMemoryOrderRepository | None = None) -> None:
        self._repository = repository or InMemoryOrderRepository()

    def read(self, order_id: str) -> str:
        if not _ORDER_ID.fullmatch(order_id):
            raise InvalidResourceURIError("Expected an order ID in the format ORD-1234")

        order = self._repository.get(order_id)
        return json.dumps(
            {
                "order_id": order.order_id,
                "status": order.status,
                "item_count": order.item_count,
                "currency": order.currency,
            },
            separators=(",", ":"),
            sort_keys=True,
        )
