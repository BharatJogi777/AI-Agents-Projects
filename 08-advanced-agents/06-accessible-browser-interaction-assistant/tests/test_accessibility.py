import pytest
from app.accessibility import UIAction,validate_action,prepare_action_plan
def test_plan_is_not_executed():
 a=UIAction("button","Save","click","https://app.example/save")
 p=prepare_action_plan([a],{"click"},{"app.example"})
 assert p["requires_user_confirmation"] and not p["executed"]
def test_rejects_unlabelled_target():
 with pytest.raises(ValueError): validate_action(UIAction("button","","click","https://app.example"),{"click"},{"app.example"})
def test_rejects_unknown_operation():
 with pytest.raises(ValueError): validate_action(UIAction("button","Save","type","https://app.example"),{"click"},{"app.example"})
