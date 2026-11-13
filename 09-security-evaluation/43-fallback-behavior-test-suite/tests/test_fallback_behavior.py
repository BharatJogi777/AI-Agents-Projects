import pytest
from app.fallback_behavior import Attempt,evaluate_fallbacks
def test_fallback_selects_first_success():
 r=evaluate_fallbacks([Attempt("primary",False,"timeout"),Attempt("secondary",True),Attempt("last",True)])
 assert r.selected_provider=="secondary" and r.attempts==2 and r.skipped_after_success==("last",)
def test_all_fail_and_duplicate_provider():
 assert evaluate_fallbacks([Attempt("a",False),Attempt("b",False)]).exhausted
 with pytest.raises(ValueError): evaluate_fallbacks([Attempt("a",False),Attempt("a",True)])
