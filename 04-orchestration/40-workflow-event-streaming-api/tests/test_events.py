import pytest
from app.events import EventStream

def test_ordered_events_and_replay_cursor():
    s=EventStream(); s.publish("wf","started",{}); s.publish("wf","step",{"n":1})
    assert s.latest_sequence("wf") == 2
    assert s.replay("wf",after_sequence=1)[0].sequence == 2

def test_validation_and_limit():
    s=EventStream()
    with pytest.raises(ValueError): s.publish("","event",{})
    with pytest.raises(ValueError): s.replay("wf",limit=0)
