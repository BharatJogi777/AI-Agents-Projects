from app import LoopDetector,evaluate_stop,StopDecision


def test_repeated_state_detected_after_configured_repeats():
    d=LoopDetector(max_repeats=2)
    assert not d.observe({"tool":"search","q":"x"}).stop
    assert not d.observe({"tool":"search","q":"x"}).stop
    decision=d.observe({"q":"x","tool":"search"})
    assert decision==StopDecision(True,"repeated_state")


def test_state_order_does_not_change_fingerprint():
    assert LoopDetector.fingerprint({"a":1,"b":2})==LoopDetector.fingerprint({"b":2,"a":1})


def test_history_is_bounded():
    d=LoopDetector(max_repeats=2,history_size=3)
    for n in range(10): d.observe({"n":n})
    assert len(d._recent)==3


def test_stop_priority_is_deterministic():
    assert evaluate_stop(final_answer=True,cancelled=True,deadline_exceeded=False,step_count=9,max_steps=5).reason=="cancelled"
    assert evaluate_stop(final_answer=False,cancelled=False,deadline_exceeded=True,step_count=9,max_steps=5).reason=="deadline_exceeded"
    assert evaluate_stop(final_answer=True,cancelled=False,deadline_exceeded=False,step_count=1,max_steps=5).reason=="final_answer"


def test_step_limit_and_continue():
    assert evaluate_stop(final_answer=False,cancelled=False,deadline_exceeded=False,step_count=3,max_steps=3).reason=="step_limit"
    assert evaluate_stop(final_answer=False,cancelled=False,deadline_exceeded=False,step_count=1,max_steps=3).reason=="continue"
