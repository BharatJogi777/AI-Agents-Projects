import pytest
from app.python_review import review
def test_mutable_default_and_eval():
 r=review("def f(x=[]):\n return eval('x')")
 assert len(r)==2 and {x["severity"] for x in r}=={"high"}
def test_bare_except(): assert review("try:\n pass\nexcept:\n pass")[0]["severity"]=="warning"
def test_syntax_error(): assert review("def (")[0]["severity"]=="error"
