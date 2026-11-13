from app.drill import plan_drill
import pytest

def test_production_drill_has_explicit_safety_gate():
    result=plan_drill("payments",rto_minutes=30,rpo_minutes=5,tier="critical",production_exercise=True)
    assert any("change approval" in item.lower() for item in result.safety_gates)
    assert any("Production failover" in item for item in result.exercises)

def test_rejects_invalid_tier():
    with pytest.raises(ValueError): plan_drill("payments",rto_minutes=30,rpo_minutes=5,tier="gold")
