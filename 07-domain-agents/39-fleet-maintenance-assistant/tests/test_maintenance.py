from datetime import date
import pytest
from app.maintenance import Vehicle,assess_maintenance
def test_due_by_distance():
 r=assess_maintenance([Vehicle("V1",12000,10000,2000,date(2026,1,1),365)],date(2026,1,2))
 assert r["vehicles"][0]["maintenance_due"] and not r["work_order_created"]
def test_rejects_future_service_date():
 with pytest.raises(ValueError): assess_maintenance([Vehicle("V1",100,0,100,date(2027,1,1),365)],date(2026,1,1))
