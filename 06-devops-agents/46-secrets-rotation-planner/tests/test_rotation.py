from app.rotation import plan_rotation
import pytest

def test_orders_dependency_before_consumer():
    result=plan_rotation([{"secret_id":"api","owner":"team-a","dependents":["db"]},{"secret_id":"db","owner":"team-b","dependents":[]}])
    assert [x.secret_id for x in result]==["db","api"]

def test_detects_dependency_cycle():
    with pytest.raises(ValueError): plan_rotation([{"secret_id":"a","owner":"x","dependents":["b"]},{"secret_id":"b","owner":"y","dependents":["a"]}])
