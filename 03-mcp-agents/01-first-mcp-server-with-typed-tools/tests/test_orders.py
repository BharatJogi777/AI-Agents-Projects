import pytest

from app.domain.orders import (
    OrderValidationError,
    calculate_order_total,
    get_order_status,
)


def test_calculates_total_with_default_tax() -> None:
    result = calculate_order_total(quantity=2, unit_price=100)
    assert result.as_dict() == {
        "quantity": 2,
        "unit_price": "100.00",
        "subtotal": "200.00",
        "tax": "36.00",
        "total": "236.00",
    }


def test_calculates_total_with_custom_tax_and_rounding() -> None:
    result = calculate_order_total(quantity=3, unit_price=19.995, tax_rate=0)
    assert result.subtotal == "59.99"
    assert result.tax == "0.00"
    assert result.total == "59.99"


@pytest.mark.parametrize(
    ("quantity", "unit_price", "tax_rate"),
    [
        (0, 10, 0.18),
        (10_001, 10, 0.18),
        (True, 10, 0.18),
        (2, 0, 0.18),
        (2, -1, 0.18),
        (2, 10, -0.1),
        (2, 10, 1.1),
        (2, float("nan"), 0.18),
        (2, float("inf"), 0.18),
    ],
)
def test_rejects_invalid_order_inputs(
    quantity: int, unit_price: float, tax_rate: float
) -> None:
    with pytest.raises(OrderValidationError):
        calculate_order_total(quantity, unit_price, tax_rate)


def test_returns_known_order_status() -> None:
    assert get_order_status(" ord-1001 ") == {
        "order_id": "ORD-1001",
        "status": "processing",
    }


@pytest.mark.parametrize("order_id", ["", "missing", "x" * 33, None])
def test_rejects_unknown_or_invalid_order_id(order_id: str | None) -> None:
    with pytest.raises(OrderValidationError):
        get_order_status(order_id)  # type: ignore[arg-type]
