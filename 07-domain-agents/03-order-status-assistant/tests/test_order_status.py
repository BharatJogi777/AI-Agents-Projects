from app.order_status import get_order_status
import pytest

def test_formats_shipped_order_tracking():
    result=get_order_status({"order_id":"o-1","status":"shipped","tracking_reference":"trk-9"})
    assert "trk-9" in result.customer_message

def test_rejects_unknown_status():
    with pytest.raises(ValueError): get_order_status({"order_id":"o-1","status":"teleported"})
