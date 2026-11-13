import pytest
from app.demand import DemandObservation,forecast
def test_moving_average():
 r=forecast([DemandObservation("p1",10),DemandObservation("p2",20),DemandObservation("p3",30)],2,5)
 assert r["baseline_units"]==25 and r["suggested_plan_units"]==30 and not r["purchase_order_created"]
def test_invalid_window():
 with pytest.raises(ValueError): forecast([DemandObservation("p1",1)],2)
