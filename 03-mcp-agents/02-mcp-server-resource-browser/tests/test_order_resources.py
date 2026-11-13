import json

import pytest

from app.repositories.orders import OrderNotFoundError
from app.services.order_resources import InvalidResourceURIError, OrderResourceService


def test_reads_known_order_as_json() -> None:
    payload = json.loads(OrderResourceService().read("ORD-1001"))

    assert payload == {
        "order_id": "ORD-1001",
        "status": "processing",
        "item_count": 3,
        "currency": "INR",
    }


@pytest.mark.parametrize("order_id", ["", "../etc/passwd", "ord-1001", "ORD-1"])
def test_rejects_invalid_resource_identifier(order_id: str) -> None:
    with pytest.raises(InvalidResourceURIError):
        OrderResourceService().read(order_id)


def test_unknown_but_well_formed_order_is_not_found() -> None:
    with pytest.raises(OrderNotFoundError, match="not found"):
        OrderResourceService().read("ORD-9999")
