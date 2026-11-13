import pytest
from app.timeline import Event,build_timeline
def test_sorts_events_and_flags_low_confidence():
 r=build_timeline(20,[Event(8,"end","Ending",.99),Event(2,"start","Beginning",.5)])
 assert r["events"][0]["label"]=="start" and r["review_indices"]==[0]
def test_rejects_event_outside_duration():
 with pytest.raises(ValueError): build_timeline(10,[Event(11,"x","y",.9)])
def test_rejects_invalid_confidence():
 with pytest.raises(ValueError): build_timeline(10,[Event(1,"x","y",1.1)])
