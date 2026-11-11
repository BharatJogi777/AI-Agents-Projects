from plan_validator import *
def test_valid_plan_has_topological_order():
 result=validate_plan([Step("b","write",("a",)),Step("a","read")])
 assert result.valid and result.topological_order==("a","b")
def test_reject_cycle_unknown_and_critical_risk():
 assert "dependency_cycle" in validate_plan([Step("a","A",("b",)),Step("b","B",("a",))]).errors
 assert not validate_plan([Step("a","A",("missing",))]).valid
 assert not validate_plan([Step("x","delete",risk="critical")]).valid
