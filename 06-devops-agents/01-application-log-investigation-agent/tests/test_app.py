import pytest
from app.log_investigation import investigate_logs

def test_groups_repeated_signatures():
    findings=investigate_logs("ERROR timeout 123\\nERROR timeout 456\\nINFO started")
    assert findings[0].count == 2

def test_empty_log_and_invalid_limit():
    assert investigate_logs("") == []
    with pytest.raises(ValueError): investigate_logs("x",max_lines=0)
