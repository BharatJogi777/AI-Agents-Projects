from app.approval_policy import evaluate_approval

def test_requires_approval_for_high_impact():
    result = evaluate_approval(action="delete",impact="high",policy={})
    assert result["status"] == "approval_required" and not result["may_execute"]

def test_blocked_action_takes_precedence():
    result = evaluate_approval(action="wire",impact="low",policy={"blocked_actions":["wire"]})
    assert result["status"] == "blocked"
