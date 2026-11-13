from app.topic import review_topic
import pytest

def test_flags_low_replication_and_infinite_retention():
    out=review_topic("events",{"replication_factor":1,"retention_ms":-1})
    assert len(out)>=2

def test_rejects_invalid_replication_factor():
    with pytest.raises(ValueError): review_topic("events",{"replication_factor":0})
