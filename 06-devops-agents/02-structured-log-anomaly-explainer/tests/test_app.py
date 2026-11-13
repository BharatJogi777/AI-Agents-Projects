import pytest
from app.log_anomaly import explain_anomalies, parse_json_lines

def test_detects_elevated_error_rate():
    records=[{"level":"error"} for _ in range(4)]+[{"level":"info"}]
    assert explain_anomalies(records,{"error":0.05})[0]["level"] == "error"

def test_json_lines_validation():
    assert parse_json_lines('{"level":"info"}') == [{"level":"info"}]
    with pytest.raises(ValueError): parse_json_lines("not json")
    with pytest.raises(ValueError): parse_json_lines('[]')
