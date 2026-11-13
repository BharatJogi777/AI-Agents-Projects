import pytest
from app.cancellation import CancellationToken

def test_parent_cancellation_propagates():
    root=CancellationToken("root"); child=CancellationToken("child"); leaf=CancellationToken("leaf")
    root.add_child(child); child.add_child(leaf); root.cancel("operator request")
    assert child.cancelled and leaf.reason == "operator request"
    with pytest.raises(RuntimeError): leaf.raise_if_cancelled()

def test_child_added_after_cancel_is_cancelled():
    root=CancellationToken("root"); root.cancel()
    child=CancellationToken("child"); root.add_child(child)
    assert child.cancelled

def test_invalid_child():
    root=CancellationToken("root")
    with pytest.raises(ValueError): root.add_child(root)
