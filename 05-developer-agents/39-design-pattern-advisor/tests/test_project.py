import pytest
from app.pattern_advisor import advise
def test_known_unknown():
 r=advise(["event_fanout","unknown"]); assert r[0]["pattern"]=="Observer" and r[1]["pattern"] is None
def test_dedup(): assert len(advise(["varying_algorithms","varying_algorithms"]))==1
def test_invalid():
 with pytest.raises(ValueError): advise("event_fanout")
