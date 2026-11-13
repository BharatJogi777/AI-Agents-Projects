from app.compensation import CompensationWorkflow, Step

def test_success_does_not_compensate():
    calls=[]
    flow=CompensationWorkflow([Step("a",lambda:calls.append("a"),lambda:calls.append("undo-a"))])
    assert flow.run().error is None and calls==["a"]

def test_failure_compensates_in_reverse():
    calls=[]
    steps=[Step("a",lambda:calls.append("a"),lambda:calls.append("undo-a")),
           Step("b",lambda:calls.append("b"),lambda:calls.append("undo-b")),
           Step("c",lambda:(_ for _ in ()).throw(ValueError("boom")),lambda:None)]
    result=CompensationWorkflow(steps).run()
    assert calls==["a","b","undo-b","undo-a"]
    assert result.compensated==("b","a") and "boom" in result.error

def test_compensation_failure_is_reported():
    steps=[Step("a",lambda:None,lambda:(_ for _ in ()).throw(RuntimeError("undo failed"))),
           Step("b",lambda:(_ for _ in ()).throw(ValueError("failed")),lambda:None)]
    assert "undo failed" in CompensationWorkflow(steps).run().error
