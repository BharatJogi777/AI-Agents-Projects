from app.returns import plan_return
import pytest

def test_blocks_undelivered_hazardous_return():
    result=plan_return("case-1",delivered=False,return_reason="damaged",item_category="battery",hazardous=True)
    assert result.blocked and result.requires_agent_approval

def test_rejects_missing_case_id():
    with pytest.raises(ValueError): plan_return("",delivered=True,return_reason="wrong size",item_category="clothing")
