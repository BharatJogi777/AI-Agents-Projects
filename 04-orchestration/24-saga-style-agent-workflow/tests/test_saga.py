from app.saga import Saga, SagaStep

def test_saga_completes_and_returns_outputs():
    saga=Saga([SagaStep("reserve",lambda:"r1",lambda:None),SagaStep("charge",lambda:"c1",lambda:None)])
    result=saga.execute()
    assert result.status=="completed" and result.outputs=={"reserve":"r1","charge":"c1"}

def test_saga_compensates_completed_steps():
    calls=[]
    steps=[SagaStep("a",lambda:calls.append("a"),lambda:calls.append("undo-a")),
           SagaStep("b",lambda:calls.append("b"),lambda:calls.append("undo-b")),
           SagaStep("c",lambda:1/0,lambda:None)]
    result=Saga(steps).execute()
    assert result.status=="compensated" and calls==["a","b","undo-b","undo-a"]

def test_compensation_failure_is_visible():
    steps=[SagaStep("a",lambda:None,lambda:1/0),SagaStep("b",lambda:1/0,lambda:None)]
    assert Saga(steps).execute().status=="compensation_failed"
