import pytest
from app.handoff import Update, summarize_handoff

def test_sorts_updates_and_extracts_open_actions():
    result=summarize_handoff([Update("2026-01-01T01:00:00Z","a","mitigated"),Update("2026-01-01T00:00:00Z","b","restart database","open","db-oncall")])
    assert result["timeline"][0]["author"] == "b"
    assert result["open_actions"][0]["owner"] == "db-oncall"

def test_rejects_timezone_missing():
    with pytest.raises(ValueError): summarize_handoff([Update("2026-01-01T00:00:00","a","x")])
