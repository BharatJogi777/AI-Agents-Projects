from app.health import investigate_targets
import pytest

def test_flags_unhealthy_target():
    findings=investigate_targets([{"id":"i-1","state":"unhealthy","reason":"Target.Timeout"}])
    assert findings[0].severity=="high"

def test_rejects_duplicate_target_ids():
    with pytest.raises(ValueError): investigate_targets([{"id":"x","state":"healthy"},{"id":"x","state":"healthy"}])
