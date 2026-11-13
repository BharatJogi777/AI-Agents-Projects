import pytest
from app.route import Stop,validate_route
def test_capacity_check():
 r=validate_route([Stop("A",12.9,77.5,3),Stop("B",13.0,77.6,2)],6)
 assert r["total_demand"]==5 and r["capacity_feasible"] and not r["route_optimized"]
def test_invalid_coordinates():
 with pytest.raises(ValueError): validate_route([Stop("A",100,0,1)],5)
