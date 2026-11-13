from app.inventory import analyze_inventory
import pytest

def test_detects_public_and_unattached_resources():
    result = analyze_inventory([{"id":"vol-1","type":"ebs-volume","attached":False,"public":True}])
    assert {x.severity for x in result} == {"high", "medium"}

def test_rejects_duplicate_ids():
    with pytest.raises(ValueError): analyze_inventory([{"id":"x","type":"s3"},{"id":"x","type":"s3"}])
