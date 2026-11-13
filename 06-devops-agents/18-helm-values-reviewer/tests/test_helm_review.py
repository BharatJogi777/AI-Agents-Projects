import pytest
from app.helm_review import review_values

def test_flags_latest_and_missing_resources():
    codes={x["code"] for x in review_values({"image":{"tag":"latest"}})}
    assert {"MUTABLE_IMAGE_TAG","MISSING_RESOURCE_REQUESTS","LOW_REPLICAS"} <= codes

def test_rejects_invalid_replicas():
    with pytest.raises(ValueError): review_values({"replicaCount":-1})
