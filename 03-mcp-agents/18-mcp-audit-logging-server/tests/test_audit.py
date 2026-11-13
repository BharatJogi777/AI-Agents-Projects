import json
import pytest
from app.audit import JsonlAuditLog

def test_writes_allowlisted_fields_only(tmp_path):
    path = tmp_path / "logs" / "audit.jsonl"
    JsonlAuditLog(path).write({"principal":"agent","tool":"orders.read","decision":"allow","arguments":{"secret":"x"}})
    record = json.loads(path.read_text())
    assert record["tool"] == "orders.read"
    assert "arguments" not in record
    assert path.stat().st_mode & 0o777 == 0o600

def test_rejects_invalid_duration(tmp_path):
    with pytest.raises(ValueError):
        JsonlAuditLog(tmp_path / "audit.jsonl").write({"duration_ms":-1})
