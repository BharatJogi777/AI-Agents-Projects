from app import Citation,verify_citations
def test_exact_quote():
 r=verify_citations([Citation("a","exact evidence"),Citation("a","fabricated")],{"a":"An exact evidence string."}); assert [x.valid for x in r]==[True,False]
def test_missing_source(): assert not verify_citations([Citation("missing","quote")],{})[0].valid
def test_empty_quote(): assert not verify_citations([Citation("a"," ")],{"a":"text"})[0].valid
