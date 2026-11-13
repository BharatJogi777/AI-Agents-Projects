from app.idempotency import IdempotentStepRunner

def test_repeated_call_replays_result_without_action():
    runner=IdempotentStepRunner(); calls=[]
    first=runner.run("w","charge",{"amount":10},lambda:calls.append(1) or {"payment":"p1"})
    second=runner.run("w","charge",{"amount":10},lambda:calls.append(2))
    assert first.result==second.result and not first.replayed and second.replayed and calls==[1]

def test_different_input_has_different_key():
    runner=IdempotentStepRunner()
    a=runner.run("w","step",{"x":1},lambda:1)
    b=runner.run("w","step",{"x":2},lambda:2)
    assert a.key!=b.key

def test_action_failure_is_not_cached():
    runner=IdempotentStepRunner()
    def fail(): raise RuntimeError("no")
    import pytest
    with pytest.raises(RuntimeError): runner.run("w","step",{},fail)
    assert runner.run("w","step",{},lambda:"ok").result=="ok"
