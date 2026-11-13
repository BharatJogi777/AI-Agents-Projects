from app.backlog import diagnose_backlog
import pytest

def test_detects_growing_backlog_and_dead_letters():
    out=diagnose_backlog({"backlog":500,"previous_backlog":300,"arrivals_per_minute":50,"processed_per_minute":20,"dead_letter_count":2})
    assert len(out)==2

def test_rejects_negative_counts():
    with pytest.raises(ValueError): diagnose_backlog({"backlog":-1})
