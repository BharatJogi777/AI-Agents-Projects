import pytest
from app.runbook_retrieval import RunbookSection, retrieve_runbooks

def test_retrieval_preserves_reference():
    docs=[RunbookSection("RB-1","Restart API","Check health then restart deployment","runbooks/api.md#restart")]
    assert retrieve_runbooks("restart API",docs)[0]["reference"] == "runbooks/api.md#restart"

def test_empty_query_rejected():
    with pytest.raises(ValueError): retrieve_runbooks(" ",[])
