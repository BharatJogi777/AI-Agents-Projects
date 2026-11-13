import pytest
from app.mobile import plan_action, authorize_execution

def test_state_change_requires_confirmation_and_permission():
    plan=plan_action("set_preference","notifications",{"enabled":"true"})
    assert not authorize_execution(plan,user_confirmed=False,granted_permissions={"notifications"})
    assert authorize_execution(plan,user_confirmed=True,granted_permissions={"notifications"})
    assert not authorize_execution(plan,user_confirmed=True,granted_permissions=set())

def test_rejects_unknown_action():
    with pytest.raises(ValueError):
        plan_action("delete_everything","storage")
