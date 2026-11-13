import pytest
from app.go_review import review
def test_reports_goroutine_and_panic():
 r=review("go func() {}()\npanic(\"bad\")")
 assert len(r)==2 and {x["severity"] for x in r}=={"warning"}
def test_line_numbers(): assert review("package p\npanic(1)")[0]["line"]==2
def test_empty():
 with pytest.raises(ValueError): review(" ")
