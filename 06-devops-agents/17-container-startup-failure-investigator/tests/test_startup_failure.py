import pytest
from app.startup_failure import investigate_startup

def test_detects_oom():
    result=investigate_startup({"name":"api","state":"exited","exit_code":137})
    assert result["category"] == "OUT_OF_MEMORY"

def test_requires_container_identity():
    with pytest.raises(ValueError): investigate_startup({"state":"running"})
