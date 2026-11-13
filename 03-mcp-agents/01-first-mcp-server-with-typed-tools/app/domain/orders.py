"""Deterministic order-domain operations; intentionally independent of MCP."""

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import StrEnum


class OrderValidationError(ValueError):
    """Raised when an order request violates a domain constraint."""


class OrderStatus(StrEnum):
    ACCEPTED = "accepted"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


@dataclass(frozen=True, slots=True)
class OrderTotal:
    quantity: int
    unit_price: str
    subtotal: str
    tax: str
    total: str

    def as_dict(self) -> dict[str, int | str]:
        return asdict(self)


_SAMPLE_ORDERS: dict[str, OrderStatus] = {
    "ORD-1001": OrderStatus.PROCESSING,
    "ORD-1002": OrderStatus.SHIPPED,
    "ORD-1003": OrderStatus.DELIVERED,
}


def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_order_total(
    quantity: int,
    unit_price: float,
    tax_rate: float = 0.18,
) -> OrderTotal:
    """Calculate a total after validating untrusted tool arguments."""
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise OrderValidationError("quantity must be an integer")
    if not 1 <= quantity <= 10_000:
        raise OrderValidationError("quantity must be between 1 and 10000")
    try:
        price = Decimal(str(unit_price))
        rate = Decimal(str(tax_rate))
    except Exception as exc:
        raise OrderValidationError("unit_price and tax_rate must be valid numbers") from exc
    if not price.is_finite() or not Decimal("0") < price <= Decimal("1000000"):
        raise OrderValidationError("unit_price must be greater than 0 and at most 1000000")
    if not rate.is_finite() or not Decimal("0") <= rate <= Decimal("1"):
        raise OrderValidationError("tax_rate must be between 0 and 1")

    subtotal = _money(price * quantity)
    tax = _money(subtotal * rate)
    total = _money(subtotal + tax)
    return OrderTotal(
        quantity=quantity,
        unit_price=f"{_money(price):.2f}",
        subtotal=f"{subtotal:.2f}",
        tax=f"{tax:.2f}",
        total=f"{total:.2f}",
    )


def get_order_status(order_id: str) -> dict[str, str]:
    """Return a read-only sample order status."""
    normalized = order_id.strip().upper() if isinstance(order_id, str) else ""
    if not normalized or len(normalized) > 32:
        raise OrderValidationError("order_id must contain between 1 and 32 characters")
    status = _SAMPLE_ORDERS.get(normalized)
    if status is None:
        raise OrderValidationError(f"unknown order_id: {normalized}")
    return {"order_id": normalized, "status": status.value}
