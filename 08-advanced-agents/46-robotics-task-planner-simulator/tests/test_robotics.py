import pytest
from app.robotics import Position, plan_path

def test_plans_waypoints():
    route=plan_path(Position(0,0),[Position(2,1)],width=4,height=4,obstacles=set())
    assert route[0]==Position(0,0) and route[-1]==Position(2,1)

def test_rejects_blocked_route():
    with pytest.raises(ValueError):
        plan_path(Position(0,0),[Position(2,0)],width=4,height=4,obstacles={Position(1,0)})
