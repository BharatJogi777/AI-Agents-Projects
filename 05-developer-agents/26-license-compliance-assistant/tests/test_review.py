from app.license_audit import audit, parse_requirements
import pytest

def test_policy_flags_and_deduplicates():
    rows=[{"name":"a","license":"GPL-3.0"},{"name":"a","license":"GPL-3.0"},{"name":"b","license":"MIT"}]
    result=audit(rows)
    assert len(result)==1 and result[0].severity=="high"

def test_invalid_record():
    with pytest.raises(ValueError): audit([{"name":"x"}])

def test_requirements_parser(tmp_path):
    f=tmp_path/"requirements.txt"; f.write_text("# comment\nrequests>=2\n")
    assert parse_requirements(f)==[{"name":"requests","license":"UNKNOWN"}]
