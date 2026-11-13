from datetime import datetime,timedelta
import pytest
from app.appointments import Appointment,validate_schedule
def test_detects_provider_overlap():
 d=datetime(2026,1,1,10)
 xs=[Appointment("A","P1",d,d+timedelta(hours=1),"confirmed","DR1"),Appointment("B","P2",d+timedelta(minutes=30),d+timedelta(hours=2),"requested","DR1")]
 assert validate_schedule(xs)["conflict_count"]==1
def test_rejects_invalid_interval():
 d=datetime(2026,1,1)
 with pytest.raises(ValueError): validate_schedule([Appointment("A","P",d,d,"requested","DR")])
