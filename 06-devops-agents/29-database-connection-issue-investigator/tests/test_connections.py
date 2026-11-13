from app.connections import investigate_connections
import pytest

def test_detects_pool_saturation_and_waiters():
    result=investigate_connections({"active":95,"max_connections":100,"waiting":3})
    assert len(result)==2

def test_rejects_negative_metrics():
    with pytest.raises(ValueError): investigate_connections({"timeouts":-1})
