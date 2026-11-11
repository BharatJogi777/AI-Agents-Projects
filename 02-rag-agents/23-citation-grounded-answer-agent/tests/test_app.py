import pytest
from app import Claim,Source,build_grounded_answer
def test_build():
 a=build_grounded_answer([Claim("The service uses retries.",("doc-1",))],[Source("doc-1","Retry policy is enabled.")]); assert "[doc-1]" in a.answer and a.source_ids==("doc-1",)
def test_multiple_claims_are_separate_lines():
 a=build_grounded_answer([Claim("First.",("a",)),Claim("Second.",("b",))],[Source("a","A"),Source("b","B")]); assert a.answer=="First. [a]\nSecond. [b]"
def test_unknown_source_rejected():
 with pytest.raises(ValueError): build_grounded_answer([Claim("Claim",("missing",))],[Source("doc","text")])
def test_uncited_claim_rejected():
 with pytest.raises(ValueError): build_grounded_answer([Claim("Claim",())],[Source("doc","text")])
