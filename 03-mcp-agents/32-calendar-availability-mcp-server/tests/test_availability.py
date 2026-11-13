from datetime import datetime,timezone,timedelta
import pytest
from app.availability import Event,free_slots

def dt(hour): return datetime(2026,1,1,hour,tzinfo=timezone.utc)

def test_merges_overlapping_events_and_returns_gaps():
    slots=free_slots(dt(9),dt(17),[Event(dt(10),dt(11)),Event(dt(10, )+timedelta(minutes=30),dt(12)),Event(dt(14),dt(15))])
    assert [(s.start.hour,s.end.hour) for s in slots]==[(9,10),(12,14),(15,17)]

def test_rejects_naive_or_reversed_window():
    with pytest.raises(ValueError): free_slots(datetime(2026,1,1,9),datetime(2026,1,1,10),[])
    with pytest.raises(ValueError): free_slots(dt(11),dt(10),[])
