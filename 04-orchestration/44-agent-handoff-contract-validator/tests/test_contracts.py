import pytest
from app.contracts import Field, HandoffContract

def test_contract_accepts_valid_payload():
    contract = HandoffContract("v1", (Field("task_id", str), Field("priority", int, False)))
    assert contract.validate({"task_id": "t-1", "priority": 2}) == []

def test_contract_reports_missing_type_and_extra_fields():
    contract = HandoffContract("v1", (Field("task_id", str),))
    errors = contract.validate({"task_id": 9, "extra": True})
    assert len(errors) == 2
    with pytest.raises(ValueError): contract.assert_valid({"task_id": 9})
