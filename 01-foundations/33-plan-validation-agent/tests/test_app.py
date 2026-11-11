from app import *
def test_valid():assert validate_plan([Step("a","read"),Step("b","write",("a",))]).valid
def test_cycle_and_unknown():
 assert "dependency_cycle" in validate_plan([Step("a","A",("b",)),Step("b","B",("a",))]).errors
 assert not validate_plan([Step("a","A",("x",))]).valid
def test_risk():assert not validate_plan([Step("x","delete",risk="critical")]).valid
