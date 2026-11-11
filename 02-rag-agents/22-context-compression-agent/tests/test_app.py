import pytest
from app import Evidence,compress_context
def test_compress_preserves_exact_spans():
 src="First sentence. Important fact here! Last sentence."; r=compress_context("fact",[Evidence("d",src)],lambda q,s:1 if "Important" in s else .1,25); assert len(r)==1 and r[0].text=="Important fact here!" and src[r[0].start:r[0].end]==r[0].text
def test_newlines_split_sentences():
 r=compress_context("q",[Evidence("d","first line\nsecond line")],lambda q,s:1); assert [x.text for x in r]==["first line","second line"]
def test_budget_and_validation():
 assert compress_context("q",[Evidence("d","long sentence.")],lambda q,s:1,2)==[]
 with pytest.raises(ValueError): compress_context("",[],lambda q,s:1)
