import pytest
from app.approval import ApprovalGate

def test_approval_is_tool_scoped_and_single_use():
    gate=ApprovalGate(); gate.request("a1","delete_file","user")
    with pytest.raises(PermissionError): gate.approve_and_execute("a1","send_email",lambda: "sent")
    assert gate.approve_and_execute("a1","delete_file",lambda x:x,"ok") == "ok"
    with pytest.raises(PermissionError): gate.approve_and_execute("a1","delete_file",lambda: None)

def test_deny():
    gate=ApprovalGate(); gate.request("a","tool","user"); assert gate.deny("a")
