import pytest
from app.replay import EventJournal, ReplayError

def reducer(state, event): return state + event.payload["n"]

def test_replay_and_checkpoint():
    journal = EventJournal(); journal.append("add", {"n": 2}); journal.append("add", {"n": 3})
    assert journal.replay(0, reducer) == 5
    assert journal.checkpoint(reducer, 0) == (2, 5)
    assert [e.sequence for e in journal.events(1)] == [2]

def test_invalid_cursor_and_name():
    journal = EventJournal()
    with pytest.raises(ValueError): journal.append(" ", {})
    with pytest.raises(ReplayError): journal.replay(0, reducer, until=1)
