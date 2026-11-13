import pytest
from app.refactor_plan import plan
def test_order():
 r=plan("billing",["extract repository"]); assert r[0].title=="Establish baseline" and r[-1].title=="Review and stage rollout"
def test_requires_goals():
 with pytest.raises(ValueError): plan("billing",[])
