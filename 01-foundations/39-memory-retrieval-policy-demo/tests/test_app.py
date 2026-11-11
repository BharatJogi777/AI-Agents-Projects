from app import *
def test_filters():
 ms=[Memory("a","python concise answers",True,.9,90),Memory("b","python",False,1,99),Memory("c","python private",True,1,99,sensitive=True),Memory("d","python expired",True,.9,99,100)]
 assert [m.id for m in retrieve("python",ms,100)]==["a"]
def test_no_overlap():assert not retrieve("unknown",[Memory("a","python",True,1,1)],10)
