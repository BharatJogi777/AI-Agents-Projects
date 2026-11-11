import pytest
from app import SearchHit,reciprocal_rank_fusion
def test_fusion():
 r=reciprocal_rank_fusion({"lex":[SearchHit("a",9,"lex"),SearchHit("b",7,"lex")],"vec":[SearchHit("b",.9,"vec"),SearchHit("a",.8,"vec")]}); assert r[0].id=="a" and set(r[0].ranks)=={"lex","vec"}
def test_invalid():
 with pytest.raises(ValueError): reciprocal_rank_fusion({},0)
