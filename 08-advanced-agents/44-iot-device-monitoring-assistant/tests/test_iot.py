import pytest
from datetime import datetime,timezone,timedelta
from app.iot import Reading, inspect_readings

def test_flags_out_of_range_and_stale_reading():
    now=datetime.now(timezone.utc)
    reading=Reading("sensor-1","temperature",50,now-timedelta(minutes=10))
    findings=inspect_readings([reading],thresholds={"temperature":(0,40)},now=now)
    assert {f.severity for f in findings}=={"warning","critical"}

def test_requires_timezone_aware_timestamps():
    now=datetime.now(timezone.utc)
    reading=Reading("sensor-1","temperature",20,datetime(2026,1,1))
    with pytest.raises(ValueError):
        inspect_readings([reading],thresholds={"temperature":(0,40)},now=now)
