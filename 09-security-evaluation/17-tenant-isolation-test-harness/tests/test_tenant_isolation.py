import pytest
from app.tenant_isolation import Record, check_isolation

def test_all_records_belong_to_tenant():
    report = check_isolation("a", [Record("1","a"), Record("2","a")])
    assert report.passed and not report.leaked_record_ids

def test_detects_cross_tenant_rows():
    report = check_isolation("a", [Record("1","a"), Record("2","b")])
    assert not report.passed and report.leaked_record_ids == ("2",)

def test_requires_tenant():
    with pytest.raises(ValueError):
        check_isolation(" ", [])
