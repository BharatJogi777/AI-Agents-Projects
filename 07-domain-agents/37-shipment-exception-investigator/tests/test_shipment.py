from datetime import datetime,timedelta
import pytest
from app.shipment import Shipment,investigate
def test_flags_overdue_shipment():
 now=datetime(2026,1,2,12)
 r=investigate([Shipment("S1",now-timedelta(hours=2),None,"in_transit","event-1")],now)
 assert r["shipments"][0]["exception"]=="overdue" and r["shipments"][0]["human_follow_up"]
def test_rejects_duplicate():
 now=datetime(2026,1,2)
 s=Shipment("S1",now,None,"in_transit","e")
 with pytest.raises(ValueError): investigate([s,s],now)
