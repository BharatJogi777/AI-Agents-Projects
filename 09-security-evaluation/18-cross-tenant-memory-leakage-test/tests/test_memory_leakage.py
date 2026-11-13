import pytest
from app.memory_leakage import Memory, audit_memory_retrieval

def test_flags_foreign_memory_without_content():
    findings = audit_memory_retrieval("tenant-a", [Memory("m1","tenant-b","private text")])
    assert len(findings) == 1 and findings[0].reason == "tenant mismatch"
    assert not hasattr(findings[0], "content")

def test_accepts_owned_memory():
    assert audit_memory_retrieval("a", [Memory("m","a","x")]) == ()

def test_requires_tenant():
    with pytest.raises(ValueError):
        audit_memory_retrieval("", [])
