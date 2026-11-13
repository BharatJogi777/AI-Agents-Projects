from datetime import datetime
import pytest
from app.scheduling import Slot,find_common_slots
def test_finds_common_free_windows():
 w=Slot(datetime(2026,1,1,9),datetime(2026,1,1,12))
 r=find_common_slots({"A":[Slot(datetime(2026,1,1,10),datetime(2026,1,1,11))],"B":[]},30,w)
 assert r==[Slot(datetime(2026,1,1,9),datetime(2026,1,1,10)),Slot(datetime(2026,1,1,11),datetime(2026,1,1,12))]
def test_invalid_window_rejected():
 with pytest.raises(ValueError): find_common_slots({},30,Slot(datetime(2026,1,1,12),datetime(2026,1,1,9)))
