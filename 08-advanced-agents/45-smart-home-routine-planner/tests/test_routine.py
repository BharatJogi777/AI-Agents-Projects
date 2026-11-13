import pytest
from app.routine import RoutineAction, validate_routine, approval_summary

def test_orders_actions_by_time():
    actions=[RoutineAction("lamp","off",120),RoutineAction("lamp","on",60)]
    result=validate_routine(actions,allowed_devices={"lamp"},allowed_commands={"on","off"})
    assert [a.scheduled_minute for a in result]==[60,120]
    assert approval_summary(result,allowed_devices={"lamp"},allowed_commands={"on","off"})[0].startswith("01:00")

def test_rejects_conflict_and_unknown_device():
    with pytest.raises(ValueError):
        validate_routine([RoutineAction("lamp","on",10),RoutineAction("lamp","off",10)],allowed_devices={"lamp"},allowed_commands={"on","off"})
    with pytest.raises(ValueError):
        validate_routine([RoutineAction("door","lock",10)],allowed_devices={"lamp"},allowed_commands={"on","off"})
